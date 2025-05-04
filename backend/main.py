from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
from pathlib import Path

import models
import schemas
import database
import moderation

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Content Publishing Platform",
    description="A platform for creating and publishing blog posts with AI moderation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories for static files and templates if they don't exist
# Use relative paths from where the script is running
current_dir = Path(__file__).parent
static_dir = current_dir / "static"
templates_dir = current_dir / "templates"

static_dir.mkdir(exist_ok=True)
templates_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Set up templates
templates = Jinja2Templates(directory=templates_dir)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create a new draft blog post."""
    db_post = models.Post(
        title=post.title,
        content=post.content,
        status="draft"
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(
    status: Optional[str] = Query(None, regex="^(draft|flagged|approved|published)$"),
    db: Session = Depends(get_db)
):
    """List all posts with optional status filter."""
    query = db.query(models.Post)
    if status:
        query = query.filter(models.Post.status == status)
    return query.all()


@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """View a specific post by ID."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts/{post_id}/submit/", response_model=schemas.Post)
def submit_post_for_review(post_id: int, db: Session = Depends(get_db)):
    """Submit the post for AI moderation review."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft posts can be submitted for review")
    
    # Run enhanced moderation checks
    moderation_result = moderation.check_content(post.content, post.title)
    
    # Store the quality score
    post.quality_score = moderation_result.get("quality_score", 0)
    
    # Store full moderation data for advanced features
    post.moderation_data = moderation_result
    
    # Store warnings as comma-separated string
    if moderation_result.get("warnings"):
        post.warnings = ", ".join(moderation_result["warnings"])
    
    if moderation_result["approved"]:
        post.status = "approved"
        post.flagged_reasons = None
    else:
        post.status = "flagged"
        post.flagged_reasons = ", ".join(moderation_result["reasons"])
    
    db.commit()
    db.refresh(post)
    return post


@app.patch("/posts/{post_id}/publish/", response_model=schemas.Post)
def publish_post(post_id: int, db: Session = Depends(get_db)):
    """Publish an approved post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.status != "approved":
        raise HTTPException(status_code=400, detail="Only approved posts can be published")
    
    # Update status and set published timestamp
    post.status = "published"
    post.published_at = datetime.now()
    
    db.commit()
    db.refresh(post)
    return post


@app.patch("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    """Update a draft or flagged post."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.status == "published":
        raise HTTPException(status_code=400, detail="Published posts cannot be edited")
    
    if db_post.status == "approved":
        # If updating an approved post, set back to draft
        db_post.status = "draft"
    
    # Update post fields
    if post_update.title is not None:
        db_post.title = post_update.title
    if post_update.content is not None:
        db_post.content = post_update.content
    if post_update.tags is not None:
        db_post.tags = post_update.tags
    
    # Clear any previous moderation data when content is updated
    if post_update.content is not None:
        db_post.moderation_data = None
        db_post.quality_score = None
        db_post.warnings = None
        db_post.flagged_reasons = None
    
    db.commit()
    db.refresh(db_post)
    return db_post


@app.get("/stats/", response_model=schemas.PostStats)
def get_post_stats(db: Session = Depends(get_db)):
    """Get statistics about posts in the platform."""
    total = db.query(models.Post).count()
    draft = db.query(models.Post).filter(models.Post.status == "draft").count()
    flagged = db.query(models.Post).filter(models.Post.status == "flagged").count()
    approved = db.query(models.Post).filter(models.Post.status == "approved").count()
    published = db.query(models.Post).filter(models.Post.status == "published").count()
    
    return {
        "total": total,
        "draft": draft,
        "flagged": flagged,
        "approved": approved,
        "published": published
    }


@app.get("/posts/{post_id}/ai-suggestions/", response_model=Dict[str, List[str]])
def get_ai_suggestions(post_id: int, db: Session = Depends(get_db)):
    """Get AI-powered suggestions for improving a post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Generate suggestions if they don't exist yet
    if not post.moderation_data or "suggestions" not in post.moderation_data:
        suggestions = moderation.generate_improvement_suggestions(post.content, post.title)
    else:
        suggestions = post.moderation_data["suggestions"]
    
    return suggestions


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    """Homepage with content publishing platform interface."""
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
