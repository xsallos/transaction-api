from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi import status
from fastapi.responses import JSONResponse

from .controllers.report import router as report_router
from .controllers.transaction import router as transaction_router
from .core.database import Base, engine


def init_db_context():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db_context()


app.include_router(transaction_router, tags=["Transactions"])
app.include_router(report_router, tags=["Reports"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Invalid input",
            "details": jsonable_encoder(exc.errors())
        },
    )


@app.get("/health-check")
def root():
    return {"application": "ok"}
