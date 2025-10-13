from pydantic import BaseModel
from datetime import datetime

# --- ベースとなるスキーマ ---
class HistoryBase(BaseModel):
    keyword: str
    category: str
    summary: str
    details: str

# --- データ作成時に使用するスキーマ ---
class HistoryCreate(HistoryBase):
    pass

# --- データ読み取り時に使用するスキーマ (DBの全フィールドを含む) ---
class History(HistoryBase):
    id: int

    class Config:
        orm_mode = True # SQLAlchemyモデルをPydanticモデルに変換可能にする
