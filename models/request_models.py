from typing import Optional

from pydantic import BaseModel, Field
from uuid import UUID


class CrudeOilDataModelPost(BaseModel):
    year: int
    month: int
    origin_name: str = Field(alias="originName")
    origin_type_name: str = Field(alias="originTypeName")
    destination_name: str = Field(alias="destinationName")
    destination_type_name: str = Field(alias="destinationTypeName")
    grade_name: str = Field(alias="gradeName")
    quantity: int

    class Config:
        validate_by_name = True
        from_attributes = True


class CrudeOilDataModelPut(CrudeOilDataModelPost):
    pass


class CrudeOilDataModelFlexible(BaseModel):
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


class CrudeOilDataModelPatch(CrudeOilDataModelFlexible):
    pass


class CrudeOilDataModelFilter(CrudeOilDataModelFlexible):
    uuid: Optional[UUID] = Field(default=None, alias="uuid")
    pass


# class CrudeOilDataModelPatch(BaseModel):
#     # Unique Identifiers
#     year: int
#     month: int
#     origin_name: str = Field(alias="originName")
#     destination_name: str = Field(alias="destinationName")
#     grade_name: str = Field(alias="gradeName")
#
#     # Non Unique Identifiers
#     origin_type_name: Optional[str] = Field(default=None, alias="originTypeName")
#     destination_type_name: Optional[str] = Field(
#         default=None, alias="destinationTypeName"
#     )
#     quantity: Optional[int] = Field(default=None)
#
#     class Config:
#         validate_by_name = True
#         from_attributes = True
