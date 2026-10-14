from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas import TestCreate
from backend.app.schemas import TestResponse
from backend.app.models import Test,Base
from backend.app.database import get_db

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/", response_model=list[TestResponse])
async def test_check(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Test))
    return result.scalars().all()


@router.get("/{test_id}", response_model=TestResponse)
async def test_get(test_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@router.post("/", response_model=TestResponse)
async def test_create(
    data: TestCreate,
    db: AsyncSession = Depends(get_db)
):

    test = Test(
        jmeno=data.jmeno,
        prijmeni=data.prijmeni
    )

    db.add(test)
    await db.commit()
    print(test)

    return {
        "id": test.id,
        "jmeno": test.jmeno,
        "prijmeni": test.prijmeni
    }