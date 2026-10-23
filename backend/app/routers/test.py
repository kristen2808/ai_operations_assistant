from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas import TestCreate
from backend.app.schemas import TestResponse
from backend.app.models import Test
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


@router.put("/{test_id}", response_model=TestResponse)
async def test_update(
    test_id: int,
    data: TestCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")

    test.jmeno = data.jmeno
    test.prijmeni = data.prijmeni
    test.email = data.email
    await db.commit()
    return test


@router.delete("/{test_id}", status_code=204, response_class=Response)
async def test_delete(test_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")

    await db.delete(test)
    await db.commit()
    return Response(status_code=204)


@router.post("/", response_model=TestResponse)
async def test_create(
    data: TestCreate,
    db: AsyncSession = Depends(get_db)
):

    test = Test(
        jmeno=data.jmeno,
        prijmeni=data.prijmeni,
        email=data.email,
    )

    db.add(test)
    await db.commit()
    return test
