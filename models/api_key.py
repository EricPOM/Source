from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from .platform import Base, AIPlatform # Import Base from platform.py
from .business_unit import BusinessUnit # Import BusinessUnit

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    # api_key_value MUST be encrypted before saving to the database.
    # It should be decrypted after loading if needed internally, but not for API responses.
    api_key_value = Column(String, nullable=False, unique=True)  # Suitable for base64 encoded encrypted data
    description = Column(String)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # New fields for rate limiting and rotation
    last_reset_time = Column(DateTime(timezone=True), nullable=True, server_default=func.now()) # Tracks start of current usage window
    last_selected_at = Column(DateTime(timezone=True), nullable=True) # Tracks when this key was last given out
    last_used_at = Column(DateTime(timezone=True), nullable=True) # Tracks when this key was last confirmed used (via logs)
    
    current_usage_requests = Column(Integer, default=0, nullable=False)
    current_usage_tokens = Column(Integer, default=0, nullable=False)
    
    rate_limit_requests_per_minute = Column(Integer, nullable=True) # Max requests allowed in the window
    # rate_limit_tokens_per_minute = Column(Integer, nullable=True) # Max tokens allowed (optional, not explicitly requested for now)

    platform_id = Column(Integer, ForeignKey("ai_platforms.id"), nullable=False)
    business_unit_id = Column(Integer, ForeignKey("business_units.id"), nullable=False)

    platform = relationship("AIPlatform", back_populates="api_keys")
    business_unit = relationship("BusinessUnit", back_populates="api_keys")
