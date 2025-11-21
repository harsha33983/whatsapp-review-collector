from sqlalchemy.orm import Session
import models, schemas

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).order_by(models.Review.created_at.desc()).offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
