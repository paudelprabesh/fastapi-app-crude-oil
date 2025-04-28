import logging
from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import bll.crude_oil_imports as bll
from dependencies import get_db
from models.request_models import (
    CrudeOilDataModelFilter,
    CrudeOilDataModelPatch,
    CrudeOilDataModelPost,
    CrudeOilDataModelPut,
)
from models.response_models import (
    DataCreatedResponseModel,
    DataUpdateResponseModel,
    FailureResponseModel,
    MultipleDataCreatedResponseModel,
    PaginatedResponseModel,
    SingleDataGetResponseModel,
    SingleDataRetrieveNotFoundResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
)

router = APIRouter(tags=["US crude oil imports"])

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@router.get(
    "/crude-oil-imports/",
    status_code=status.HTTP_200_OK,
    response_model=Union[PaginatedResponseModel, FailureResponseModel],
)
async def get_paginated_crude_oil_imports(
    skip: int = 0,
    limit: int = 500,
    filters: CrudeOilDataModelFilter = Depends(CrudeOilDataModelFilter),
    db: AsyncSession = Depends(get_db),
) -> Union[PaginatedResponseModel, FailureResponseModel]:
    """
    Retrieves a paginated list of crude oil import records based on the filters.

    This endpoint allows clients to retrieve crude oil import data in chunks,
    supporting efficient retrieval of large datasets.  It supports filtering
    of the data, and returns a consistent structure.
    ### Parameters

    - `skip` (int, optional): The number of records to skip before returning data. Defaults to 0.

    - `limit` (int, optional): The maximum number of records to return. Defaults to 500.

    - `filters` (CrudeOilDataModelFilter, optional):  Filters to apply to the query.
                Unset values are ignored and not included in the filter.

    ### Returns:

    - `Union[PaginatedResponseModel, FailureResponseModel]`: A `PaginatedResponseModel` containing the requested crude oil
     import data if the request is successful. A FailureResponseModel is returned if an error occurs during processing.

    ### Note: Response samples are also shown below by swagger.
    """
    try:
        paginated_data = await bll.get_paginated_crude_oil_imports(
            db, skip=skip, limit=limit, filters=filters
        )
        return PaginatedResponseModel(data=paginated_data)
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


@router.get(
    "/crude-oil-imports/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Union[
        SingleDataGetResponseModel | SingleDataRetrieveNotFoundResponseModel
    ],
)
async def get_crude_oil_imports_from_uuid(
    uuid: UUID, db: AsyncSession = Depends(get_db)
) -> Union[SingleDataGetResponseModel, SingleDataRetrieveNotFoundResponseModel]:
    """
    Retrieves a single crude oil import record by its UUID.

    This endpoint allows clients to retrieve a specific crude oil import
    record using its unique identifier.

    ### Parameters

    - `uuid` (UUID, required): The UUID of the crude oil import record to retrieve.

    ### Returns:

    - `Union[SingleDataGetResponseModel  |  SingleDataRetrieveNotFoundResponseModel]`:
        A SingleDataGetResponseModel containing the requested crude oil import data
        if the record is found. A SingleDataRetrieveNotFoundResponseModel is returned
        if the record is not found.

    ### Note: Response samples are also shown below by swagger.
    """
    result = await bll.get_crude_oil_from_uuid(db, uuid)
    if not result:
        return SingleDataRetrieveNotFoundResponseModel()
    return SingleDataGetResponseModel(data=result)


@router.post(
    "/crude-oil-imports/",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[DataCreatedResponseModel, FailureResponseModel],
)
async def insert(
    crude_oil_data: CrudeOilDataModelPost, db: AsyncSession = Depends(get_db)
) -> Union[DataCreatedResponseModel, FailureResponseModel]:
    """
    Inserts a new crude oil import record into the database.
    This endpoint allows to create a new crude oil import record.
    Make sure that the `month` is in range of `[1,12]` and `year` in range of `[1900, 2100]`

    ### Parameters

    - `crude_oil_data` (CrudeOilDataModelPost, required): The data for the new crude oil import record.
    This should be a JSON object conforming to the CrudeOilDataModelPost schema.

    ### Returns:

    - `Union[DataCreatedResponseModel, FailureResponseModel]`:
        A DataCreatedResponseModel containing the newly created crude oil import
        data if the record is created successfully. A FailureResponseModel is returned
        if an error occurs during processing.

    ### Note: A sample format will be prepopulated, we only need to edit the values.
    """
    try:
        inserted_record = await bll.insert_one_data_into_database(db, crude_oil_data)
        return DataCreatedResponseModel(data=inserted_record.model_dump())
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


@router.post(
    "/crude-oil-imports/bulk",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[MultipleDataCreatedResponseModel, FailureResponseModel],
)
async def insert_bulk(
    crude_oil_data_list: List[CrudeOilDataModelPost], db: AsyncSession = Depends(get_db)
) -> Union[MultipleDataCreatedResponseModel, FailureResponseModel]:
    """
    Inserts multiple new crude oil import records into the database in bulk.

    This endpoint allows clients to create multiple new crude oil import records
    simultaneously, improving efficiency for large data uploads.

    Make sure that for each data, the `month` is in range of `[1,12]` and `year` in range of `[1900, 2100]`

    ### Parameters

    - `crude_oil_data_list` (List[CrudeOilDataModelPost], required): A list of data
            objects for the new crude oil import records. Each item in the list
            should be a JSON object conforming to the CrudeOilDataModelPost schema.

    ### Returns:

    - `Union[MultipleDataCreatedResponseModel  |  FailureResponseModel]`:
        A MultipleDataCreatedResponseModel containing the newly created crude oil import
        data if the records are created successfully. A FailureResponseModel is returned
        if an error occurs during processing.

    ### Note: A sample format will be prepopulated, we only need to edit the values.
    """
    try:
        inserted_data = await bll.insert_multiple_data_into_database(
            db, crude_oil_data_list
        )
        return MultipleDataCreatedResponseModel(data=inserted_data)
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


@router.patch(
    "/crude-oil-imports/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Union[
        DataUpdateResponseModel,
        SingleDataUpdateUnsuccessfulResponseModel,
        FailureResponseModel,
    ],
)
async def patch_crude_oil_import(
    uuid: UUID, patch_data: CrudeOilDataModelPatch, db: AsyncSession = Depends(get_db)
) -> Union[
    DataUpdateResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
    FailureResponseModel,
]:
    """
        Updates an existing crude oil import record identified by its UUID.

    This endpoint allows clients to modify specific fields of an existing crude oil
    import record.  It uses the PATCH method, so only the fields provided in the
    request will be updated, leaving other fields unchanged.

    Make sure that the `month` is in range of `[1,12]` and `year` in range of `[1900, 2100]`

    ### Parameters

    - `uuid` (UUID, required): The unique identifier (UUID) of the crude oil import record to be updated.

    - `patch_data` (CrudeOilDataModelPatch, required):  An object containing the fields and new values to update.
            Only include the fields that need to be changed.  Omitted fields will retain their original values.
            The object should conform to the CrudeOilDataModelPatch schema.

    ### Returns:

    - `Union[DataUpdateResponseModel, SingleDataUpdateUnsuccessfulResponseModel, FailureResponseModel]`:
        -  A DataUpdateResponseModel containing the updated data if the record is successfully updated.
        -  A SingleDataUpdateUnsuccessfulResponseModel with a message "No such record exists." if the provided UUID does not match any existing record.
        -  A FailureResponseModel if an error occurs during processing.

    ### Note: A sample format will be prepopulated, we only need to edit the values.
    """
    try:
        patched_data = await bll.patch_crude_oil_import_from_uuid(db, uuid, patch_data)
        if not patched_data:
            return SingleDataUpdateUnsuccessfulResponseModel(
                message="No such record exists."
            )
        return DataUpdateResponseModel(data=patched_data)
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


@router.put(
    "/crude-oil-imports/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Union[
        DataUpdateResponseModel,
        SingleDataUpdateUnsuccessfulResponseModel,
        FailureResponseModel,
    ],
)
async def update_crude_oil_import(
    uuid: UUID, update_data: CrudeOilDataModelPut, db: AsyncSession = Depends(get_db)
) -> Union[
    DataUpdateResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
    FailureResponseModel,
]:
    """
    Replaces an existing crude oil import record entirely with new data.

    This endpoint allows clients to update all fields of an existing crude oil import record.
    It uses the PUT method, so the provided data will completely replace the existing
    record.  There should be no missing fields and should confirm to `CrudeOilDataModelPut` schema.

    Make sure that the `month` is in range of `[1,12]` and `year` in range of `[1900, 2100]`

    ### Parameters

    - `uuid` (UUID, required): The unique identifier (UUID) of the crude oil import record to be updated.

    - `update_data` (CrudeOilDataModelPut, required): An object containing the complete set of new data
            for the crude oil import record.  All fields of the record will be replaced
            with the values provided in this object. The object should conform to the
            CrudeOilDataModelPut schema.

    ### Returns:

    - `Union[DataUpdateResponseModel, SingleDataUpdateUnsuccessfulResponseModel, FailureResponseModel]`:
        -  A DataUpdateResponseModel containing the updated data if the record is successfully updated.
        -  A SingleDataUpdateUnsuccessfulResponseModel with a message "No such record exists." if the provided UUID does not match any existing record.
        -  A FailureResponseModel if an error occurs during processing.

    ### Note: A sample format will be prepopulated, we only need to edit the values.
    """
    try:
        updated_data = await bll.put_update_crude_oil_import_from_uuid(
            db, uuid, update_data
        )
        if not updated_data:
            return SingleDataUpdateUnsuccessfulResponseModel(
                message="No such record exists."
            )
        return DataUpdateResponseModel(data=updated_data)
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


@router.delete(
    "/crude-oil-imports/{uuid}",
    status_code=status.HTTP_200_OK,
    response_model=Union[
        DataUpdateResponseModel,
        SingleDataUpdateUnsuccessfulResponseModel,
        FailureResponseModel,
    ],
)
async def update_crude_oil_import(
    uuid: UUID, db: AsyncSession = Depends(get_db)
) -> Union[
    DataUpdateResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
    FailureResponseModel,
]:
    """
    Deletes an existing crude oil import record identified by its UUID.

    This endpoint permanently removes a crude oil import record from the database.

    ### Parameters

    - `uuid` (UUID, required): The unique identifier (UUID) of the crude oil import record to be deleted.

    ### Returns:

    - `Union[DataUpdateResponseModel, SingleDataUpdateUnsuccessfulResponseModel, FailureResponseModel]`:
        -  A DataUpdateResponseModel containing the data of the deleted record if the record is successfully deleted.
        -  A SingleDataUpdateUnsuccessfulResponseModel with a message "No such record exists." if the provided UUID does not match any existing record.
        -  A FailureResponseModel if an error occurs during processing.

    """

    try:
        deleted_data = await bll.delete_data_from_uuid(db, uuid)
        if not deleted_data:
            return SingleDataUpdateUnsuccessfulResponseModel(
                message="No such record exists."
            )
        return DataUpdateResponseModel(data=deleted_data)
    except HTTPException as he:
        logger.error(f"HTTPException {str(he)}")
        return FailureResponseModel(status=he.status_code, message=he.detail)
    except Exception as e:
        logger.error(f"Unknown Error {str(e)}")
        return FailureResponseModel(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
        )


# @router.patch(
#     "/crude-oil-imports/",
#     status_code=status.HTTP_200_OK,
#     response_model=DataUpdateResponseModel,
# )
# async def patch_crude_oil_imports(
#         patch_data: CrudeOilDataModelPatch,
#         db: AsyncSession = Depends(get_db),
# ):
#     try:
#         patched_data = await bll.patch_crude_oil_import(
#             db, patch_data
#         )
#         return DataUpdateResponseModel(data=patched_data)
#     except HTTPException as he:
#         logger.error(f"HTTPException {str(he)}")
#         return FailureResponseModel(status=he.status_code, message=he.detail)
#     except Exception as e:
#         logger.error(f"Unknown Error {str(e)}")
#         return FailureResponseModel(
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR, message="Unknown Error"
#         )
