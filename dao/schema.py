import uuid as uuid_lib
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CrudeOilImports(Base):
    __tablename__ = "crude_oil_imports"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid_lib.uuid4, unique=True, nullable=False, index=True
    )
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    origin_name: Mapped[str] = mapped_column(ForeignKey("origins.name"), index=True)
    origin_type_name: Mapped[str] = mapped_column(ForeignKey("origin_types.name"))
    destination_name: Mapped[str] = mapped_column(ForeignKey("destinations.name"))
    destination_type_name: Mapped[str] = mapped_column(ForeignKey("destination_types.name"))
    grade_name: Mapped[str] = mapped_column(ForeignKey("grades.name"))
    quantity: Mapped[int] = mapped_column()

    origin: Mapped["Origin"] = relationship(back_populates="imports")
    origin_type: Mapped["OriginType"] = relationship(back_populates="imports")
    destination: Mapped["Destination"] = relationship(back_populates="imports")
    destination_type: Mapped["DestinationType"] = relationship(back_populates="imports")
    grade: Mapped["Grade"] = relationship(back_populates="imports")


class Origin(Base):
    __tablename__ = "origins"
    name: Mapped[str] = mapped_column(String, primary_key=True, nullable=False, index=True)
    imports: Mapped[List["CrudeOilImports"]] = relationship(back_populates="origin")


class Destination(Base):
    __tablename__ = "destinations"
    name: Mapped[str] = mapped_column(String, primary_key=True, nullable=False, index=True)
    imports: Mapped[List["CrudeOilImports"]] = relationship(back_populates="destination")


class OriginType(Base):
    __tablename__ = "origin_types"
    name: Mapped[str] = mapped_column(String, primary_key=True, nullable=False, index=True)
    imports: Mapped[List["CrudeOilImports"]] = relationship(back_populates="origin_type")


class DestinationType(Base):
    __tablename__ = "destination_types"
    name: Mapped[str] = mapped_column(String, primary_key=True, nullable=False, index=True)
    imports: Mapped[List["CrudeOilImports"]] = relationship(back_populates="destination_type")

class Grade(Base):
    __tablename__ = "grades"
    name: Mapped[str] = mapped_column(String, primary_key=True, unique=True, nullable=False, index=True)
    imports: Mapped[List["CrudeOilImports"]] = relationship(back_populates="grade")


    def __repr__(self):
        return "<Destination Type: name='{self.name}'>"
