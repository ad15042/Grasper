from sqlalchemy.orm import Session
import models, schemas

def get_history(db: Session, history_id: int):
    """ 指定されたIDの履歴を1件取得 """
    return db.query(models.GenerationHistory).filter(models.GenerationHistory.id == history_id).first()

def get_all_histories(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    term: str = None,
    category_large: str = None,
    category_medium: str = None,
    category_small: str = None,
    is_favorite: bool = None
):
    """ 全ての履歴を取得 """
    query = db.query(models.GenerationHistory)

    if term:
        query = query.filter(models.GenerationHistory.term.contains(term))
    if category_large:
        query = query.filter(models.GenerationHistory.category_large == category_large)
    if category_medium:
        query = query.filter(models.GenerationHistory.category_medium == category_medium)
    if category_small:
        query = query.filter(models.GenerationHistory.category_small == category_small)
    if is_favorite is not None:
        query = query.filter(models.GenerationHistory.is_favorite == is_favorite)

    return query.order_by(models.GenerationHistory.id.desc()).offset(skip).limit(limit).all()

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

def get_unique_categories(db: Session):
    """ ユニークなカテゴリを取得 """
    large_categories = db.query(models.GenerationHistory.category_large).distinct().all()
    medium_categories = db.query(models.GenerationHistory.category_medium).distinct().all()
    return {
        "large": [c[0] for c in large_categories],
        "medium": [c[0] for c in medium_categories]
    }

