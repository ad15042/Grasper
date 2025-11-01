from sqlalchemy.orm import Session
import models, schemas

def get_history(db: Session, history_id: int):
    """ 指定されたIDの履歴を1件取得 """
    return db.query(models.GenerationHistory).filter(models.GenerationHistory.id == history_id).first()

def get_all_histories(db: Session, skip: int = 0, limit: int = 100):
    """ 全ての履歴を取得 """
    return db.query(models.GenerationHistory).order_by(models.GenerationHistory.id.desc()).offset(skip).limit(limit).all()

def create_history(db: Session, history: schemas.HistoryCreate):
    """ 新しい履歴を作成 """
    db_history = models.GenerationHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def delete_history(db: Session, history_id: int):
    """ 指定されたIDの履歴を削除 """
    db_history = db.query(models.GenerationHistory).filter(models.GenerationHistory.id == history_id).first()
    if db_history:
        db.delete(db_history)
        db.commit()
        return db_history
    return None

def toggle_favorite(db: Session, history_id: int):
    """ 指定されたIDの履歴のお気に入り状態を切り替え """
    db_history = db.query(models.GenerationHistory).filter(models.GenerationHistory.id == history_id).first()
    if db_history:
        db_history.is_favorite = not db_history.is_favorite
        db.commit()
        db.refresh(db_history)
        return db_history
    return None

