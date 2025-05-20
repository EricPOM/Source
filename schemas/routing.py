from pydantic import BaseModel

class KeySelectionResponse(BaseModel):
    api_key_id: int
    api_key_value: str  # Actual key value, for trusted SDK use
    platform_id: int
    business_unit_id: int
    # model_name: Optional[str] = None # Could be added if the selection logic uses it
    # selected_reason: Optional[str] = None # To provide context on why this key was chosen

    class Config:
        orm_mode = True # Though not directly mapping to an ORM model for response construction
