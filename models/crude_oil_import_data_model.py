from typing import Optional, List

from pydantic import BaseModel, Field


# class CrudeOilDataModel(BaseModel):
#     year: int
#     month: int
#     origin_name: str = Field(alias="originName")
#     origin_type_name: str = Field(alias="originTypeName")
#     destination_name: str = Field(alias="destinationName")
#     destination_type_name: str = Field(alias="destinationTypeName")
#     grade_name: str = Field(alias="gradeName")
#     quantity: int
#
#     class Config:
#         validate_by_name = True
#         from_attributes = True


class CrudeOilDataModel(BaseModel):
    year: Optional[int] = Field(default=None)
    month: Optional[int] = Field(default=None)
    origin_name: Optional[str] = Field(default=None, alias="originName")
    origin_type_name: Optional[str] = Field(default=None, alias="originTypeName")
    destination_name: Optional[str] = Field(default=None, alias="destinationName")
    destination_type_name: Optional[str] = Field(
        default=None, alias="destinationTypeName"
    )
    grade_name: Optional[str] = Field(default=None, alias="gradeName")
    quantity: Optional[int] = Field(default=None)

    class Config:
        validate_by_name = True
        from_attributes = True


class PaginatedMetaData(BaseModel):
    skip: int
    limit: int
    total: int


class PaginatedCrudeOilDataModel(BaseModel):
    metadata: PaginatedMetaData
    paginated_data: List[CrudeOilDataModel]
