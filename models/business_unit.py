from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BusinessUnit(Base):
    __tablename__ = "business_units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    contact_email = Column(String, nullable=True) # New field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    api_keys = relationship("APIKey", back_populates="business_unit")
