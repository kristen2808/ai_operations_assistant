from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    jmeno: Mapped[str] = mapped_column(String(100))
    prijmeni: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

class DiagnosticRun(Base):
    __tablename__ = "diagnostic_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    check_type: Mapped[str] = mapped_column(String(100), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    result: Mapped[dict | list] = mapped_column(JSONB, nullable=False)
