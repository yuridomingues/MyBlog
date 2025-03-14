from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import models, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/articles", tags=["Articles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.ArticleOut])
def get_articles(
    db: Session = Depends(get_db),
    published: Optional[bool] = None
):
    """Get all articles, with an optional published filter."""
    query = db.query(models.Article)
    if published is not None:
        query = query.filter(models.Article.published == published)
    return query.order_by(models.Article.created_at.desc()).all()

@router.get("/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found."
        )
    return article

@router.post("/", response_model=schemas.ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    new_article = models.Article(
        title=article.title,
        content=article.content,
        published=article.published,
    )
    if article.published:
        new_article.published_at = datetime.utcnow()

    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.put("/{article_id}", response_model=schemas.ArticleOut)
def update_article(article_id: int, updated_data: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    existing_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not existing_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found."
        )

    existing_article.title = updated_data.title
    existing_article.content = updated_data.content
    existing_article.published = updated_data.published
    existing_article.published_at = datetime.utcnow() if updated_data.published else None

    db.commit()
    db.refresh(existing_article)
    return existing_article

@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found."
        )

    db.delete(article)
    db.commit()
    return {"detail": "Artigo deleted successfully."}
