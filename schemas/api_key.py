from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base schema for APIKey, containing common attributes
class APIKeyBase(BaseModel):
    description: Optional[str] = None
    platform_id: int
    business_unit_id: int
    expires_at: Optional[datetime] = None
    is_active: bool = True
    last_reset_time: Optional[datetime] = None
    last_selected_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    current_usage_requests: Optional[int] = 0 # Informational, actual value from DB
    current_usage_tokens: Optional[int] = 0 # Informational, actual value from DB
    rate_limit_requests_per_minute: Optional[int] = None

# Schema for creating a new APIKey.
# api_key_value is write-only and should not be in responses.
class APIKeyCreate(APIKeyBase):
    api_key_value: str = Field(..., description="The API key value. This will be encrypted before storage.")

# Schema for updating an existing APIKey.
# Only certain fields might be updatable, and api_key_value might be handled separately.
class APIKeyUpdate(BaseModel):
    description: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None
    rate_limit_requests_per_minute: Optional[int] = None # Allow updating rate limit
    # platform_id and business_unit_id are typically not updated after creation.
    # api_key_value is not directly updatable; a new key should be issued.

# Schema for reading/returning APIKey data.
# Crucially, api_key_value is NOT included.
class APIKeyRead(APIKeyBase):
    id: int
    # We add a field to indicate the key is masked, rather than sending the actual key.
    api_key_display: str = Field("********", description="Masked API key value.")
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Schema for the response when a new APIKey is created.
# This might include the original api_key_value if it's a one-time display scenario,
# but generally, it's better practice not to return it, or return a hash/masked version.
# For this exercise, we will NOT return the raw api_key_value.
class APIKeyCreateResponse(APIKeyRead):
    pass # Inherits all fields from APIKeyRead, ensuring no raw key is exposed.
