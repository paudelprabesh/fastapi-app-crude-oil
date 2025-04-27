import logging

from fastapi import HTTPException
from typing import List, Union

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.crude_oil_import_data_model import (
    CrudeOilDataModel,
    CrudeOilDataModel,
)
import bll.crude_oil_imports as bll

from dependencies import get_db
from models.response_models import (
    DataCreatedResponseModel,
    FailureResponseModel,
    MultipleDataCreatedResponseModel,
    PaginatedResponseModel,
)

router = APIRouter(tags=["US crude oil imports"])

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@router.post("/crude-oil-imports/", status_code=status.HTTP_201_CREATED)
async def insert(
    crude_oil_data: CrudeOilDataModel, db: AsyncSession = Depends(get_db)
) -> Union[DataCreatedResponseModel, FailureResponseModel]:
    try:
        inserted_record = await bll.insert_one_data_into_database(db, crude_oil_data)
        return DataCreatedResponseModel(data=inserted_record)
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
async def insert(
    crude_oil_data_list: List[CrudeOilDataModel], db: AsyncSession = Depends(get_db)
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


@router.get(
    "/crude-oil-imports/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponseModel,
)
async def get_paginated_crude_oil_imports(
    skip: int = 0,
    limit: int = 500,
    filters: CrudeOilDataModel = Depends(CrudeOilDataModel),
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
