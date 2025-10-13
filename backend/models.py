from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    category = Column(String, index=True)
    summary = Column(Text)
    details = Column(Text)
