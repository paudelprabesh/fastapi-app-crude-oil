import logging
import uuid
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dao.schema import CrudeOilImportsSchema
from models.request_models import CrudeOilDataModelPost
from models.response_models import CrudeOilDataResponseModel

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def add_a_record_to_database(db: AsyncSession, data: CrudeOilDataModelPost):
    try:
        row = CrudeOilImportsSchema(**data.model_dump(), uuid=uuid.uuid4())
        db.add(row)
        return row
    except Exception as e:
        error_text = "Something went wrong adding record to db (lazy)."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def get_records_from_db(db: AsyncSession, filters: dict, skip=0, limit=20):
    try:
        query = (
            select(CrudeOilImportsSchema)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit)
            .order_by(CrudeOilImportsSchema.id)
        )
        results = (await db.execute(query)).scalars().all()
        return results
    except Exception as e:
        error_text = "Something went wrong reading from db."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def count_records_in_db(db: AsyncSession, filters: dict):
    try:
        query = select(CrudeOilImportsSchema).filter_by(**filters).subquery()
        query = select(func.count()).select_from(query)
        result = (await db.execute(query)).scalars().first()
        return result
    except Exception as e:
        error_text = "Something went wrong counting number of records in db."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def update_crude_oil_imports(db, update_data, filters) -> Optional[dict]:
    try:
        query = (
            update(CrudeOilImportsSchema)
            .where(*filters)
            .values(**update_data)
            .returning(CrudeOilImportsSchema)
        )
        result = await db.execute(query)
        updated_record = result.scalars().first()
        if not updated_record:
            await db.commit()
            return None
        updated_row = updated_record.__dict__.copy()
        await db.commit()
        return updated_row
    except Exception as e:
        await db.rollback()
        error_text = "Error while executing update query on database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def delete_crude_oil_imports(db: AsyncSession, filters: list) -> Optional[dict]:
    try:
        query = (
            delete(CrudeOilImportsSchema)
            .where(*filters)
            .returning(CrudeOilImportsSchema)
        )
        result = await db.execute(query)
        deleted_record = result.scalars().first()
        if not deleted_record:
            return None
        deleted_row = deleted_record.__dict__.copy()
        await db.commit()
        return deleted_row
    except Exception as e:
        await db.rollback()
        error_text = "Error while executing delete query on database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def insert_multiple_data_into_database(db: AsyncSession, data_list: list) -> List:
    updated = []
    for data in data_list:
        row = add_a_record_to_database(db, data)
        updated.append(row.__dict__.copy())
    try:
        await db.commit()
        return updated
    except Exception as e:
        await db.rollback()
        error_text = "Error while executing insert query on database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def insert_single_data_into_database(
    db: AsyncSession, data: CrudeOilDataModelPost
) -> dict:
    inserted_data = add_a_record_to_database(db, data)
    inserted_data = inserted_data.__dict__.copy()
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        error_text = "Error while executing insert query on database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )
    return inserted_data
