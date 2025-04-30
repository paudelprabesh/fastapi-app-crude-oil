import logging
import uuid
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from dao.schema import CrudeOilImports, Grade, Origin, Destination, OriginType, DestinationType
from models.request_models import CrudeOilDataModelPost
import uuid as uuid_lib


logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def add_a_record_to_database(db: AsyncSession, data: CrudeOilDataModelPost):
    try:
        row = CrudeOilImports(**data.model_dump(), uuid=uuid.uuid4())
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
            select(CrudeOilImports)
            .filter_by(**filters)
            .offset(skip)
            .limit(limit)
            .order_by(CrudeOilImports.id)
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
        query = select(CrudeOilImports).filter_by(**filters).subquery()
        query = select(func.count()).select_from(query)
        result = (await db.execute(query)).scalars().first()
        return result
    except Exception as e:
        error_text = "Something went wrong counting number of records in db."
        logger.error(f"{error_text} {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_text
        )


async def update_crude_oil_imports(db, update_data_model, filters) -> Optional[dict]:
    try:
        update_data = update_data_model.model_dump()
        update_data["destination_name"], update_data["destination_type_name"], update_data["grade_name"], update_data["origin_name"], update_data["origin_type_name"] = \
            await get_or_create_all_other_tables(update_data_model, db)
        update_data = {k: v for k, v in update_data_model.model_dump().items() if v is not None}
        query = (
            update(CrudeOilImports)
            .where(*filters)
            .values(**update_data)
            .returning(CrudeOilImports)
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
            delete(CrudeOilImports)
            .where(*filters)
            .returning(CrudeOilImports)
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
        row = await add_to_db_before_commit(data, db)
        updated.append(row)
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


async def get_or_create(db: AsyncSession, model, defaults=None, **kwargs):
    """

    :param db: AsyncSession
    :param model: db schema to which to get or create
    :param defaults: any default values
    :param kwargs: insert key value pairs
    :return:
    """
    # Check if object exists
    q = select(model).filter_by(**kwargs)
    result = await db.execute(q)
    instance = result.scalars().first()

    if instance:
        return instance.name
    else:
        # Create new instance
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        instance_name = instance.name[:]
        db.add(instance)
        await db.flush()
        return instance_name


async def add_to_db_before_commit(data, db):

    destination, destination_type, grade, origin, origin_type = await get_or_create_all_other_tables(data, db)

    new_import = CrudeOilImports(
        uuid=uuid_lib.uuid4(),
        year=data.year,
        month=data.month,
        quantity=data.quantity,
        origin_type_name=origin_type,
        origin_name=origin,
        destination_name=destination,
        destination_type_name=destination_type,
        grade_name=grade,
    )
    db.add(new_import)
    new_import = new_import.__dict__.copy()
    return new_import


async def get_or_create_all_other_tables(data, db):
    destination = destination_type = grade = origin = origin_type = None
    if data.origin_name:
        origin = await get_or_create(
            db, Origin, name=data.origin_name
        )
    if data.origin_type_name:
        origin_type = await get_or_create(
            db, OriginType, name=data.origin_type_name
        )
    if data.destination_name:
        destination = await get_or_create(
            db, Destination, name=data.destination_name,
        )
    if data.destination_type_name:
        destination_type = await get_or_create(
            db, DestinationType, name=data.destination_type_name
        )
    if data.grade_name:
        grade = await get_or_create(
            db, Grade, name=data.grade_name
        )
    return destination, destination_type, grade, origin, origin_type