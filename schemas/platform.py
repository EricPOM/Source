from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AIPlatformBase(BaseModel):
    name: str
    description: Optional[str] = None

class AIPlatformCreate(AIPlatformBase):
    pass

class AIPlatformUpdate(AIPlatformBase):
    pass

class AIPlatformRead(AIPlatformBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
