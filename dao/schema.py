from sqlalchemy import BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CrudeOilImportsSchema(Base):
    __tablename__ = "crude_oil_imports"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column()
    month: Mapped[int] = mapped_column()
    origin_name: Mapped[str] = mapped_column()
    origin_type_name: Mapped[str] = mapped_column()
    destination_name: Mapped[str] = mapped_column()
    destination_type_name: Mapped[str] = mapped_column()
    grade_name: Mapped[str] = mapped_column()
    quantity: Mapped[int] = mapped_column()
