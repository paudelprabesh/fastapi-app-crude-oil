import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from dao.schema import Base
from dao.session import engine
from routers.crude_oil_imports import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create the database schema during the startup of the server, if not already created.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


description = """
View, Add, Edit, and be creative with the US crude Oil Imports Data. All the endpoints are documented within.

### Design Notes :
**UUID:** UUIDs are used to identify  each records.
Instead of relying on the database's auto-generated integer IDs, we use `UUID` and hide 
the table row id from the client, which is very easy to mess up. 
For example: A mistaken id for a delete query, deletes a record. It also hides database primary key 
and how they are setup.

**Null values**: For simplicity, we don't allow null values to any records. A quick glance showed that there were no nulls
in the provided dataset, and hence assumed it to simplify design.

**Year and Month**: In addition to being `int`, they also need to be inbetween a certain range to be valid.
Year should be between `1900` and `2100`, and month should be in range of `1` and `12`.

**quantity**: `quantity` must be a positive integer.
"""

app = FastAPI(
    title="US Crude Oil Imports Data",
    description=description,
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
