from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.schemas import TestCreate
from backend.app.schemas import TestResponse
from backend.app.models import Test,Base
from backend.app.database import get_db

print(Base.metadata.tables)

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/")
async def test_check():
    return {
        "jmeno": "Milan",
        "prijmeni": "Janacek"
    }


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