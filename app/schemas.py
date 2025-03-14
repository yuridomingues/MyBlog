from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str = Field(..., example="Internet")
    content: str = Field(..., example="Bla bla bla")
    published: bool = Field(default=True)

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True