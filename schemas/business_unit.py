from pydantic import BaseModel, EmailStr # Import EmailStr for email validation
from datetime import datetime
from typing import Optional

class BusinessUnitBase(BaseModel):
    name: str
    description: Optional[str] = None
    contact_email: Optional[EmailStr] = None # New field

class BusinessUnitCreate(BusinessUnitBase):
    pass

class BusinessUnitUpdate(BusinessUnitBase):
    # Allow partial updates, so all fields should be optional
    name: Optional[str] = None
    description: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class BusinessUnitRead(BusinessUnitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # contact_email is inherited from BusinessUnitBase

    class Config:
        orm_mode = True
