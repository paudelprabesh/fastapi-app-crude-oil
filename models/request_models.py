from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CrudeOilDataModelBase(BaseModel):
    """
    Base model which has all the fields, optional.
    Subclassed according to endpoint needs.
    """

    year: Optional[int] = Field(default=None, examples=[2000], ge=1900, le=2100)
    month: Optional[int] = Field(default=None, examples=[1], ge=1, le=12)
    origin_name: Optional[str] = Field(default=None, alias="originName")
    origin_type_name: Optional[str] = Field(default=None, alias="originTypeName")
    destination_name: Optional[str] = Field(default=None, alias="destinationName")
    destination_type_name: Optional[str] = Field(
        default=None, alias="destinationTypeName"
    )
    grade_name: Optional[str] = Field(default=None, alias="gradeName")
    quantity: Optional[int] = Field(default=None, examples=[1], ge=1)

    class Config:
        validate_by_name = True
        from_attributes = True


class CrudeOilDataModelFilter(CrudeOilDataModelBase):
    pass


class CrudeOilDataModelPatch(CrudeOilDataModelBase):
    pass


class CrudeOilDataModelPost(CrudeOilDataModelBase):
    """
    Stricter model. Needs complete data to insert into the database.
    """

    year: int = Field(examples=[2000], ge=1900, le=2100)
    month: int = Field(examples=[1], ge=1, le=12)
    origin_name: str = Field(alias="originName")
    origin_type_name: str = Field(alias="originTypeName")
    destination_name: str = Field(alias="destinationName")
    destination_type_name: str = Field(alias="destinationTypeName")
    grade_name: str = Field(alias="gradeName")
    quantity: int = Field(examples=[1], ge=1)

    class Config:
        validate_by_name = True
        from_attributes = True


class CrudeOilDataModelPut(CrudeOilDataModelPost):
    pass
