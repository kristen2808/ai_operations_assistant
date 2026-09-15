from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
import sys

# Přidat backend do sys.path pokud není tam
if __name__ == "__main__":
    sys.path.insert(0, "../")

class BaseResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime = datetime.now()