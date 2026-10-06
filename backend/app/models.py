from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    jmeno: Mapped[str] = mapped_column(String(100))
    prijmeni: Mapped[str] = mapped_column(String(100))