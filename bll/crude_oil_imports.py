import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from uuid import UUID

import dal.crude_oil_imports as dal
from dao.schema import CrudeOilImportsSchema
from models.crude_oil_import_data_model import (
    CrudeOilDataModelFilter,
    CrudeOilDataModelPut,
    CrudeOilDataModelPost,
    CrudeOilDataModelPatch,
)
from models.response_models import (
    PaginatedMetaData,
    PaginatedCrudeOilDataModel,
    CrudeOilDataResponseModel,
    SingleDataRetrieveNotFoundResponseModel,
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def insert_one_data_into_database(db, data):
    inserted_data = dal.add_a_record_to_database(db, data)
    formatted_data = CrudeOilDataResponseModel.model_validate(inserted_data)
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        error_text = "Something went wrong inserting record into the database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )
    return formatted_data


async def insert_multiple_data_into_database(db, data_list):
    updated = []
    for data in data_list:
        row = dal.add_a_record_to_database(db, data)
        updated.append(row)
    updated = [CrudeOilDataResponseModel.model_validate(row) for row in updated]
    await db.commit()
    return updated


async def get_crude_oil_from_uuid(db, uuid):
    db_data = await dal.get_records_from_db(db, filters={"uuid": uuid})
    if not db_data:
        return None
    return CrudeOilDataResponseModel.model_validate(db_data[0])


async def get_paginated_crude_oil_imports(
    db: AsyncSession,
    filters: CrudeOilDataModelFilter,
    skip: int = 0,
    limit: int = 100,
) -> PaginatedCrudeOilDataModel:

    query_filters = {
        column: value
        for column, value in filters.model_dump().items()
        if value is not None
    }

    paginated_data, total = await asyncio.gather(
        dal.get_records_from_db(db=db, skip=skip, limit=limit, filters=query_filters),
        dal.count_records_in_db(db, filters=query_filters),
    )

    metadata = PaginatedMetaData(**{"total": total, "skip": skip, "limit": limit})
    return PaginatedCrudeOilDataModel(metadata=metadata, paginated_data=paginated_data)


async def patch_crude_oil_import_from_uuid(
    db: AsyncSession, uuid: UUID, patch_data_model: CrudeOilDataModelPatch
):
    updates = {k: v for k, v in patch_data_model.model_dump().items() if v is not None}
    updated_row = await dal.update_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid], update_data=updates
    )
    if not updated_row:
        return None
    return updated_row


async def put_update_crude_oil_import_from_uuid(
    db: AsyncSession, uuid: UUID, patch_data_model: CrudeOilDataModelPut
):
    updates = patch_data_model.model_dump()
    deleted_row = await dal.update_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid], update_data=updates
    )
    if not deleted_row:
        return None
    return deleted_row


# async def patch_crude_oil_import(db, patch_data_model: CrudeOilDataModelPatch):
#     unique_columns = {"year", "month", "origin_name", "destination_name", "grade_name"}
#     # filter based on unique columns
#     # dynamically can be done using
#     # filters = [getattr(CrudeOilImportsSchema, key) == value for key, value in patch_data_model.model_dump().items() if key in unique_columns]
#     filters = [
#         CrudeOilImportsSchema.year == patch_data_model.year,
#         CrudeOilImportsSchema.month == patch_data_model.month,
#         CrudeOilImportsSchema.origin_name == patch_data_model.origin_name,
#         CrudeOilImportsSchema.destination_name == patch_data_model.destination_name,
#         CrudeOilImportsSchema.grade_name == patch_data_model.grade_name,
#         ]
#     patch_data = {k: v for k, v in patch_data_model.model_dump().items() if v is not None and k not in unique_columns}
#     updated_data = await dal.patch_crude_oil_imports(db, patch_data=patch_data, filters=filters)
#     return updated_data


def delete_data_from_uuid(db: AsyncSession, uuid: UUID):
    deleted_row = dal.delete_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid]
    )
    if not deleted_row:
        return None
    return deleted_row
