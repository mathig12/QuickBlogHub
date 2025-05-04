from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, sql
from sqlalchemy.sql import func
from database import Base

class Post(Base):
    """Post model representing blog posts in the database."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(
        String, 
        CheckConstraint("status IN ('draft', 'flagged', 'approved', 'published')"),
        nullable=False,
        default="draft"
    )
    flagged_reasons = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', status='{self.status}')>"
