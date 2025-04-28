from typing import Optional

from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class CrudeOilDataModelBase(BaseModel):
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

    @field_validator("month")
    def validate_month(cls, value):
        if value is None:
            return None  # Allow None values
        if not 1 <= value <= 12:
            raise ValueError("Month must be between 1 and 12")
        return value

    @field_validator("year")
    def validate_year(cls, value):
        if value is None:
            return None  # Allow None values
        if not 1900 <= value <= 2100:  # Example range, adjust as needed
            raise ValueError("Year must be between 1900 and 2100")
        return value


class CrudeOilDataModelPost(CrudeOilDataModelBase):
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


class CrudeOilDataModelPatch(CrudeOilDataModelBase):
    pass


class CrudeOilDataModelFilter(CrudeOilDataModelBase):
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
