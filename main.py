import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.crude_oil_imports import router

from dao.schema import Base
from dao.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create the database schema during the startup of the server, if not already created.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="US Crude Oil Imports Data",
    description="View, Add, Edit, and be creative with the US crude Oil Imports Data.",
    lifespan=lifespan,
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

app.include_router(router=router)


# @app.exception_handler(RequestValidationError)
# def log_every_exception(request: Request, exception: RequestValidationError):
#     logger.error(f"Exception caught: {exception}")
#     return FailureResponseModel(
#         status=status.HTTP_422_UNPROCESSABLE_ENTITY, message=str(exception)
#     )
