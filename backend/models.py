from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, index=True, nullable=False)
    
    category_large = Column(String, nullable=False)
    category_medium = Column(String, nullable=False)
    category_small = Column(String, nullable=True)

    summary = Column(Text, nullable=False)
    details = Column(Text, nullable=False)
    
    is_favorite = Column(Boolean, default=False, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

