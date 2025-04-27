import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

import dal.crude_oil_imports as dal
from models.crude_oil_import_data_model import (
    CrudeOilDataModel,
    PaginatedCrudeOilDataModel,
    PaginatedMetaData,
)


async def insert_one_data_into_database(db, data):
    dal.add_a_record_to_database(db, data)
    await dal.commit_into_db(db)
    return data


async def insert_multiple_data_into_database(db, data_list):
    for data in data_list:
        dal.add_a_record_to_database(db, data)
    await dal.commit_into_db(db)
    return data_list


async def get_paginated_crude_oil_imports(
    db: AsyncSession,
    filters: CrudeOilDataModel,
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
