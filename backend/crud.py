from sqlalchemy.orm import Session
import models, schemas

# --- Read (単一) ---
def get_history(db: Session, history_id: int):
    return db.query(models.GeneratedContent).filter(models.GeneratedContent.id == history_id).first()

# --- Read (複数) ---
def get_histories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GeneratedContent).order_by(models.GeneratedContent.id.desc()).offset(skip).limit(limit).all()

# --- Create ---
def create_history(db: Session, keyword: str, response_data: dict):
    db_history = models.GeneratedContent(
        keyword=keyword,
        category=response_data.get("category"),
        summary=response_data.get("summary"),
        details=response_data.get("details")
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

# --- Delete ---
def delete_history(db: Session, history_id: int):
    db_history = db.query(models.GeneratedContent).filter(models.GeneratedContent.id == history_id).first()
    if db_history:
        db.delete(db_history)
        db.commit()
        return db_history
    return None
