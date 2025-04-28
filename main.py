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
##   US Crude Oil Imports Data API



This API provides access to data on US crude oil imports, allowing you to view, add, and modify records.  All endpoints 
are fully documented within the OpenAPI specification.

###   API Overview

This API enables you to:
* Retrieve crude oil import data.
* Add new crude oil import records.
* Modify existing crude oil import records.
* Delete an existing crude oil import record.

###   Design decisions:

The following design principles were applied in the development of this API:

* **Universally Unique Identifiers (UUIDs):**
    * Each crude oil import record is identified by a `UUID`. These APIs generate and use UUIDs instead of database 
      table's primary key column. These UUID cannot be set by user, but is shown to the user after creation of a record.
    `UUID` can then be used to `update` and `delete` the existing records.
    * **Rationale:**
        * **Data Integrity:** Using UUIDs significantly reduces the risk of accidentally modifying or deleting the wrong record.
          For example, a client providing an incorrect integer ID in a delete request could unintentionally delete a different record.  UUIDs make such errors far less likely.
        * **Security:** UUIDs obscure the database's primary key structure and prevent clients from inferring how records are organized or numbered. 
* **Non-Nullable Values:**
    * For simplicity and data consistency, this API does not allow to insert null values in any record fields.
    * **Rationale:**
        * The initial dataset provided contained no null values.  
        This design decision simplifies data handling and ensures that all records have complete information.
* **Data Validation:**
    * The API enforces data validation rules to ensure data quality:
        * **year:** `year` values must be integers between 1900 and 2100 (inclusive).
        * **month:** `month` values must be integers between 1 and 12 (inclusive).
        * **quantity:** `quantity` values must be positive integers.
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
