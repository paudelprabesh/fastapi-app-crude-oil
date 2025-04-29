from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

from models.request_models import CrudeOilDataModelPost


class ResponseModel(BaseModel):
    status: int
    message: str
    data: dict = Field(default_factory=dict)

    class Config:
        validate_by_name = True
        from_attributes = True


class CrudeOilDataResponseModel(CrudeOilDataModelPost):
    uuid: UUID


class SingleDataGetResponseModel(ResponseModel):
    status: int = "200"
    message: str = "Success"
    data: CrudeOilDataResponseModel


class DataCreatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: CrudeOilDataResponseModel


class FailureResponseModel(ResponseModel):
    status: int = 500
    message: str = "Unknown Error"


class MultipleDataCreatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: list[CrudeOilDataResponseModel]


class DataUpdateResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: CrudeOilDataResponseModel


class PaginatedMetaData(BaseModel):
    skip: int
    limit: int
    total: int


class PaginatedCrudeOilDataModel(BaseModel):
    metadata: PaginatedMetaData
    paginated_data: List[CrudeOilDataResponseModel]


class PaginatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: PaginatedCrudeOilDataModel


class SingleDataRetrieveNotFoundResponseModel(ResponseModel):
    status: int = 200
    message: str = "Success"
    data: dict = {}


class SingleDataUpdateUnsuccessfulResponseModel(ResponseModel):
    status: int = 400
    message: str = "Failed"
    data: dict = {}


# class SingleDataInsertUnsuccessfulResponseModel(ResponseModel):
#     status: int = 400
#     message: str = "Failed"
#     data: dict = {}
