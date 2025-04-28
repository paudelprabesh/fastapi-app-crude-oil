import uuid as uuid_lib
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class CrudeOilImportsSchema(Base):
    __tablename__ = "crude_oil_imports"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[uuid_lib.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid_lib.uuid4, unique=True, nullable=False
    )
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    origin_name: Mapped[str] = mapped_column()
    origin_type_name: Mapped[str] = mapped_column()
    destination_name: Mapped[str] = mapped_column()
    destination_type_name: Mapped[str] = mapped_column()
    grade_name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()

    # __table_args__ = (
    #     UniqueConstraint('year', 'month', 'origin_name', 'destination_name', 'grade_name', name='unique_import'),
    # )
