from pydantic import BaseModel, Field

from models.crude_oil_import_data_model import PaginatedCrudeOilDataModel


class ResponseModel(BaseModel):
    status: int
    message: str
    data: dict = Field(default_factory=dict)


class DataCreatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"


class FailureResponseModel(ResponseModel):
    status: int = 500
    message: str = "Unknown Error"


class MultipleDataCreatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: list = []


class PaginatedResponseModel(ResponseModel):
    status: int = 201
    message: str = "Success"
    data: PaginatedCrudeOilDataModel
