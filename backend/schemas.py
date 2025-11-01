from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- ベースとなるスキーマ ---
class HistoryBase(BaseModel):
    term: str
    category_large: str
    category_medium: str
    category_small: Optional[str] = None
    summary: str
    details: str

# --- データ作成時に使用するスキーマ ---
class HistoryCreate(HistoryBase):
    pass

# --- データ読み取り時に使用するスキーマ (DBの全フィールドを含む) ---
class History(HistoryBase):
    id: int
    is_favorite: bool
    created_at: datetime

    class Config:
        orm_mode = True # SQLAlchemyモデルをPydanticモデルに変換可能にする

