from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    excerpt: Optional[str] = Field(None, max_length=1000)
    author: str = Field(..., min_length=1, max_length=200)
    tags: List[str] = Field(default_factory=list)
    category: str = Field(..., min_length=1)
    cover_image: Optional[str] = None
    read_time: Optional[int] = Field(None, ge=1)
    is_published: bool = Field(default=True)
    
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    excerpt: Optional[str] = Field(None, max_length=1000)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    cover_image: Optional[str] = None
    read_time: Optional[int] = Field(None, ge=1)
    is_published: Optional[bool] = None

class ArticleResponse(BaseModel):
    id: str
    title: str
    content: str
    excerpt: Optional[str]
    author: str
    tags: List[str]
    category: str
    cover_image: Optional[str]
    read_time: Optional[int]
    is_published: bool
    views_count: int
    created_at: datetime
    updated_at: datetime
