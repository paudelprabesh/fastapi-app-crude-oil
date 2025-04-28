import asyncio
import logging
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import dal.crude_oil_imports as dal
from dao.schema import CrudeOilImportsSchema
from models.request_models import (
    CrudeOilDataModelFilter,
    CrudeOilDataModelPatch,
    CrudeOilDataModelPost,
    CrudeOilDataModelPut,
)
from models.response_models import (
    CrudeOilDataResponseModel,
    PaginatedCrudeOilDataModel,
    PaginatedMetaData,
)

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def insert_one_data_into_database(db, data: CrudeOilDataModelPost):
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
    # Only use set parameters for filtering.
    query_filters = {
        column: value
        for column, value in filters.model_dump().items()
        if value is not None
    }

    paginated_data, total = await asyncio.gather(
        dal.get_records_from_db(db=db, skip=skip, limit=limit, filters=query_filters),
        dal.count_records_in_db(db, filters=query_filters),
    )
    # Set metadata
    metadata = PaginatedMetaData(**{"total": total, "skip": skip, "limit": limit})
    return PaginatedCrudeOilDataModel(metadata=metadata, paginated_data=paginated_data)


async def patch_crude_oil_import_from_uuid(
    db: AsyncSession, uuid: UUID, patch_data_model: CrudeOilDataModelPatch
) -> Optional[CrudeOilDataResponseModel]:
    """
    :param db: sqlalchemy async session object
    :param uuid: uuid of the item being patched
    :param patch_data_model: CrudeOilDataModelPatch data model containing patch values
    :return: Optional[int, CrudeOilDataResponseModel] patched record data
    """
    # Only use set parameters for filtering.
    updates = {k: v for k, v in patch_data_model.model_dump().items() if v is not None}
    updated_row = await dal.update_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid], update_data=updates
    )
    if not updated_row:
        return None
    return updated_row


async def put_update_crude_oil_import_from_uuid(
    db: AsyncSession, uuid: UUID, patch_data_model: CrudeOilDataModelPut
) -> Optional[CrudeOilDataResponseModel]:
    """
    :param db: sqlalchemy async session object
    :param uuid: uuid of the item being patched
    :param patch_data_model: CrudeOilDataModelPatch data model containing patch values
    :return: Optional[int, CrudeOilDataResponseModel] patched record data
    """
    # No need to filter, replace all the received column values.
    updates = patch_data_model.model_dump()
    deleted_row = await dal.update_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid], update_data=updates
    )
    if not deleted_row:
        return None
    return deleted_row


async def delete_data_from_uuid(
    db: AsyncSession, uuid: UUID
) -> Optional[CrudeOilDataResponseModel]:
    deleted_row = await dal.delete_crude_oil_imports(
        db, filters=[CrudeOilImportsSchema.uuid == uuid]
    )
    if not deleted_row:
        return None
    return deleted_row
