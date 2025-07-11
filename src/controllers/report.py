from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.transaction.errors import CustomerSummaryNotFound, ProductSummaryNotFound
from src.transaction.service import TransactionService, get_transaction_service

router = APIRouter()


@router.get("/reports/customer-summary/{customer_id}")
async def get_customer_summary(
    customer_id: UUID, service: TransactionService = Depends(get_transaction_service)
):
    try:
        customer_summary_ = service.get_customer_summary(customer_id=customer_id)

        return JSONResponse(
            content=jsonable_encoder(customer_summary_), status_code=status.HTTP_200_OK
        )

    except CustomerSummaryNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.as_dict,
        )


@router.get("/reports/product-summary/{product_id}")
async def get_product_summary(
    product_id: UUID, service: TransactionService = Depends(get_transaction_service)
):
    try:
        product_summary_ = service.get_product_summary(product_id=product_id)

        return JSONResponse(
            content=jsonable_encoder(product_summary_), status_code=status.HTTP_200_OK
        )

    except ProductSummaryNotFound as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error.as_dict,
        )
