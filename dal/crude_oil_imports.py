import logging

from fastapi import HTTPException, status
from sqlalchemy import select, func

from models.crude_oil_import_data_model import CrudeOilDataModel

from dao.schema import CrudeOilImportsSchema

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


async def commit_into_db(db):
    try:
        await db.commit()
        await db.flush()
    except Exception as e:
        error_text = "Something went wrong inserting record into the database."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


def add_a_record_to_database(db, data: CrudeOilDataModel):
    try:
        row = CrudeOilImportsSchema(**data.model_dump())
        db.add(row)
        return row
    except Exception as e:
        error_text = "Something went wrong adding record to db (lazy)."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def get_records_from_db(db, skip, limit, filters):
    try:
        query = (
            select(CrudeOilImportsSchema).filter_by(**filters).offset(skip).limit(limit)
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
