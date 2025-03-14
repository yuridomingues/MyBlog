from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
import datetime


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published  = Column(Boolean, default=True)
    published_at = Column(DateTime(timezone=True), nullable=True)    
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.datetime.now)
