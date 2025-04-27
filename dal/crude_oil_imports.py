import logging

import uuid
from fastapi import HTTPException, status
from sqlalchemy import select, func, update
from sqlalchemy import delete

from sqlalchemy.ext.asyncio import AsyncSession

from models.crude_oil_import_data_model import CrudeOilDataModelFilter

from dao.schema import CrudeOilImportsSchema
from models.response_models import CrudeOilDataResponseModel

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# async def commit_into_db(db):
#     try:
#         await db.commit()
#         await db.flush()
#     except Exception as e:
#         await db.rollback()
#         error_text = "Something went wrong inserting record into the database."
#         logger.error(f"{error_text} {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
#         )


def add_a_record_to_database(db, data: CrudeOilDataModelFilter):
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


async def get_records_from_db(db, filters, skip=0, limit=20):
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


async def count_records_in_db(db, filters):
    try:
        query = select(CrudeOilImportsSchema).filter_by(**filters).subquery()
        query = select(func.count()).select_from(query)
        result = (await db.execute(query)).scalars().all()
        return result[0]
    except Exception as e:
        error_text = "Something went wrong counting number of records in db."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def update_crude_oil_imports(db, update_data, filters):
    try:
        query = (
            update(CrudeOilImportsSchema)
            .where(*filters)
            .values(**update_data)
            .returning(CrudeOilImportsSchema)
        )
        result = await db.execute(query)
        updated_record = result.scalars().all()
        if not updated_record:
            return
        updated_row = CrudeOilDataResponseModel.model_validate(updated_record[0])
        await db.commit()
        return updated_row
    except Exception as e:
        await db.rollback()
        logger.error(f"Error while executing query on database. {e}")
        raise


async def delete_crude_oil_imports(db: AsyncSession, filters: list):
    try:
        query = (
            delete(CrudeOilImportsSchema)
            .where(*filters)
            .returning(CrudeOilImportsSchema)
        )
        result = await db.execute(query)
        deleted_record = result.scalars().all()
        if not deleted_record:
            return
        deleted_row = CrudeOilDataResponseModel.model_validate(deleted_record[0])
        await db.commit()
        return deleted_row
    except Exception as e:
        await db.rollback()
        logger.error(f"Error while executing query on database. {e}")
        raise
