import logging

from fastapi import HTTPException
from typing import List, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from models.crude_oil_import_data_model import (
    CrudeOilDataModelFilter,
    CrudeOilDataModelPost,
    CrudeOilDataModelPut,
    CrudeOilDataModelPatch,
)
import bll.crude_oil_imports as bll

from dependencies import get_db
from models.response_models import (
    DataCreatedResponseModel,
    FailureResponseModel,
    MultipleDataCreatedResponseModel,
    PaginatedResponseModel,
    DataUpdateResponseModel,
    SingleDataRetrieveNotFoundResponseModel,
    SingleDataGetResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
)

router = APIRouter(tags=["US crude oil imports"])

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@router.get(
    "/crude-oil-imports/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponseModel,
)
async def get_paginated_crude_oil_imports(
    skip: int = 0,
    limit: int = 500,
    filters: CrudeOilDataModelFilter = Depends(CrudeOilDataModelFilter),
    db: AsyncSession = Depends(get_db),
):
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
    # response_model=SingleDataGetResponseModel,
)
async def get_crude_oil_imports_from_uuid(
    uuid: UUID, db: AsyncSession = Depends(get_db)
) -> Union[SingleDataGetResponseModel, SingleDataRetrieveNotFoundResponseModel]:
    result = await bll.get_crude_oil_from_uuid(db, uuid)
    if not result:
        return SingleDataRetrieveNotFoundResponseModel()
    return SingleDataGetResponseModel(data=result)


@router.post("/crude-oil-imports/", status_code=status.HTTP_201_CREATED)
async def insert(
    crude_oil_data: CrudeOilDataModelPost, db: AsyncSession = Depends(get_db)
) -> Union[DataCreatedResponseModel, FailureResponseModel]:
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
    response_model=DataUpdateResponseModel,
)
async def patch_crude_oil_import(
    uuid: UUID, patch_data: CrudeOilDataModelPatch, db: AsyncSession = Depends(get_db)
):
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
    # response_model=DataUpdateResponseModel,
)
async def update_crude_oil_import(
    uuid: UUID, update_data: CrudeOilDataModelPut, db: AsyncSession = Depends(get_db)
):
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
    # response_model=DataUpdateResponseModel,
)
async def update_crude_oil_import(
    uuid: UUID, db: AsyncSession = Depends(get_db)
) -> Union[
    DataUpdateResponseModel,
    SingleDataUpdateUnsuccessfulResponseModel,
    FailureResponseModel,
]:
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
