from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/")
async def test_check():
    return {
        "jmeno": "Milan",
        "prijmeni": "Janacek"
    }
