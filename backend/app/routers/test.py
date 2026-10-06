from fastapi import APIRouter
from backend.app.schemas import TestCreate
from backend.app.schemas import TestResponse
from backend.app.models import Test

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/")
async def test_check():
    return {
        "jmeno": "Milan",
        "prijmeni": "Janacek"
    }

@router.post("/", response_model=TestResponse)
async def test_create(data: TestCreate):

    test = Test(
        jmeno=data.jmeno,
        prijmeni=data.prijmeni
    )

    print(test)

    return {
        "id": 1,
        "jmeno": data.jmeno,
        "prijmeni": data.prijmeni
    }


