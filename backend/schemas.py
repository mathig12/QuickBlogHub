from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, List, Any
from datetime import datetime

class PostBase(BaseModel):
    """Base schema for post data."""
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    tags: Optional[str] = None  # Comma-separated tags

class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass

class PostUpdate(BaseModel):
    """Schema for updating an existing post."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[str] = None

class ModerationDetail(BaseModel):
    """Schema for detailed moderation data."""
    quality_score: float
    quality_analysis: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    suggestions: Dict[str, List[str]]
    warnings: List[str]
    moderation_timestamp: str

class Post(PostBase):
    """Schema for returning post data."""
    id: int
    status: str
    flagged_reasons: Optional[str] = None
    quality_score: Optional[float] = None
    warnings: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    moderation_data: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True  # Renamed from orm_mode in Pydantic v2
        
    @validator('status')
    def validate_status(cls, v):
        if v not in ('draft', 'flagged', 'approved', 'published'):
            raise ValueError('Invalid status')
        return v

class PostStats(BaseModel):
    """Schema for post statistics."""
    total: int
    draft: int
    flagged: int
    approved: int
    published: int
