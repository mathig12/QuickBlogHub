from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    """Base schema for post data."""
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass

class PostUpdate(BaseModel):
    """Schema for updating an existing post."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)

class Post(PostBase):
    """Schema for returning post data."""
    id: int
    status: str
    flagged_reasons: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True
        
    @validator('status')
    def validate_status(cls, v):
        if v not in ('draft', 'flagged', 'approved', 'published'):
            raise ValueError('Invalid status')
        return v
