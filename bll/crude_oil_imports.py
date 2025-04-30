import asyncio
import logging
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

import dal.crude_oil_imports as dal
from dao.schema import CrudeOilImports
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


async def insert_one_data_into_database(
    db: AsyncSession, data: CrudeOilDataModelPost
) -> Optional[CrudeOilDataResponseModel]:
    """

    :param db: Async db session sqlalchemy
    :param data: CrudeOilDataModelPost object containing values to be inserted into db
    :return: CrudeOilDataResponseModel if successful, else an error is raised
    """
    try:
        inserted_data = await dal.insert_single_data_into_database(db, data)
        formatted_data = CrudeOilDataResponseModel(**inserted_data)
    except ValidationError as e:
        logger.error(
            "Cannot create response model while using the inserted value from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"{e}")
        raise
    return formatted_data


async def insert_multiple_data_into_database(
    db: AsyncSession, data_list: list
) -> List[CrudeOilDataResponseModel]:
    """

    :param db: SQLAlchemy async db session
    :param data_list: list of updates
    :return: List[CrudeOilDataResponseModel] list of all the updates if successful, else error raised
    """
    try:
        inserted_rows = await dal.insert_multiple_data_into_database(db, data_list)
        inserted = [
            CrudeOilDataResponseModel.model_validate(row) for row in inserted_rows
        ]
        return inserted
    except ValidationError as e:
        logger.error(
            "Cannot create response model while using the inserted values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Cannot convert updated values into response model."
            "Check for inconsistencies in the db data."
            f"{e}"
        )
        raise


async def get_crude_oil_from_uuid(
    db: AsyncSession, uuid: UUID
) -> Optional[CrudeOilDataResponseModel]:
    try:
        db_data = await dal.get_records_from_db(db, filters={"uuid": uuid})
        if not db_data:
            return None
        return CrudeOilDataResponseModel.model_validate(db_data[0])
    except ValidationError as e:
        logger.error(
            "Cannot create response model while using the values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception:
        raise


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
    try:
        # Set metadata
        metadata = PaginatedMetaData(**{"total": total, "skip": skip, "limit": limit})
        return PaginatedCrudeOilDataModel(
            metadata=metadata, paginated_data=paginated_data
        )
    except ValidationError as e:
        logger.error(
            "Cannot create Paginated response model while using the values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except Exception:
        raise


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
    # updates = {k: v for k, v in patch_data_model.model_dump().items() if v is not None}
    try:
        updated_row = await dal.update_crude_oil_imports(
            db,
            filters=[CrudeOilImports.uuid == uuid],
            update_data_model=patch_data_model,
        )
        if not updated_row:
            return None
        updated_row = CrudeOilDataResponseModel.model_validate(updated_row)
        return updated_row
    except ValidationError as e:
        logger.error(
            "Cannot create response model using updated data from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Cannot create response model while getting the patched values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise


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
    # updates = patch_data_model.model_dump()
    try:
        updated_row = await dal.update_crude_oil_imports(
            db,
            filters=[CrudeOilImports.uuid == uuid],
            update_data_model=patch_data_model,
        )
        if not updated_row:
            return None
        updated_row = CrudeOilDataResponseModel.model_validate(updated_row)
        return updated_row
    except ValidationError as e:
        logger.error(
            "Cannot create response model using updated data from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Cannot create response model while getting the patched values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise


async def delete_data_from_uuid(
    db: AsyncSession, uuid: UUID
) -> Optional[CrudeOilDataResponseModel]:
    try:
        deleted_row = await dal.delete_crude_oil_imports(
            db, filters=[CrudeOilImports.uuid == uuid]
        )
        if not deleted_row:
            return None
        return CrudeOilDataResponseModel.model_validate(deleted_row)
    except ValidationError as e:
        logger.error(
            "Cannot create response model using deleted data."
            f"Please check for inconsistent data. {e}"
        )
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Cannot create response model while getting the patched values from db."
            f"Please check for inconsistent data. {e}"
        )
        raise
