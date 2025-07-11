from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from ..core.errors import RepositoryOperationalError, RepositoryUniqueConstraintError
from ..transaction.errors import (
    InvalidFileStructure,
    TransactionNotFound,
    UnsupportedTransactionFormat,
)
from ..transaction.service import TransactionService, get_transaction_service

AVAILABLE_MIME_FORMATS = ["text/csv", "application/vnd.ms-excel"]

router = APIRouter()


def _verify_file_mimetype(file: File):
    if file.content_type not in AVAILABLE_MIME_FORMATS:
        raise UnsupportedTransactionFormat


@router.get("/transactions")
async def fetch_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
    product_id: Optional[UUID] = None,
    customer_id: Optional[UUID] = None,
    service: TransactionService = Depends(get_transaction_service),
):
    paginated = service.fetch_paginated(
        page=page, page_size=page_size, product_id=product_id, customer_id=customer_id
    )

    return JSONResponse(
        content=jsonable_encoder(paginated), status_code=status.HTTP_200_OK
    )


@router.get("/transactions/{transaction_id}")
async def get_transaction_details(
    transaction_id: UUID,
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        transaction = service.get_by_id(transaction_id=transaction_id)

        return JSONResponse(
            content=jsonable_encoder(transaction), status_code=status.HTTP_201_CREATED
        )

    except TransactionNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.as_dict,
        )


@router.post("/transactions/upload")
async def upload_transaction(
    file: UploadFile = File(...),
    service: TransactionService = Depends(get_transaction_service),
):
    try:
        _verify_file_mimetype(file=file)

        file_content: bytes = await file.read()
        bulk_transaction = service.create_from_csv(content=file_content)

        status_code = None

        if bulk_transaction.success and not bulk_transaction.failure:
            status_code = status.HTTP_201_CREATED

        if bulk_transaction.success and bulk_transaction.failure:
            status_code = status.HTTP_207_MULTI_STATUS

        if not bulk_transaction.success and bulk_transaction.failure:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        if not bulk_transaction.success and not bulk_transaction.failure:
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        return JSONResponse(
            content=jsonable_encoder(bulk_transaction), status_code=status_code
        )

    except (UnsupportedTransactionFormat, InvalidFileStructure) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.as_dict,
        )

    except (RepositoryUniqueConstraintError, RepositoryOperationalError) as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error.as_dict,
        )
