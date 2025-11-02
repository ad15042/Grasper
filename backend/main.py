from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import google.generativeai as genai
import os
import json

import crud, models, schemas
from database import SessionLocal, engine, get_db

# --- Alembicを使わない場合はこの行を有効化 ---
# models.Base.metadata.create_all(bind=engine)

# --- Google Gemini API Configuration ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set.")
genai.configure(api_key=api_key)
# Geminiモデルの準備
model = genai.GenerativeModel('gemini-2.5-pro')

app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/generate", response_model=schemas.History)
def generate_and_save(request: schemas.HistoryCreate, db: Session = Depends(get_db)):
    """ Gemini APIでテキストを生成し、DBに保存する """
    try:
        # Create history entry in the database
        history_entry = crud.create_history(db=db, history=request)
        return history_entry
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-ai-response")
async def generate_ai_response(request: dict):
    term = request.get("term")
    if not term:
        raise HTTPException(status_code=400, detail="Term is required")
        
    system_prompt = f"""
    あなたは優秀なアシスタントです。ユーザーから与えられたキーワード「{term}」について、以下のJSON形式で解説を生成してください。
    他の形式での出力は避け、必ずJSON形式で出力してください。
    フィールド:
    - category_large: 最も適切な大項目カテゴリを一つ設定してください。（例: IT, 医療, 経済）
    - category_medium: 中項目カテゴリを一つ設定してください。（例: プログラミング, 創薬, 金融）
    - category_small: (任意) 小項目カテゴリがあれば設定してください。（例: Python, 分子標的薬, 株式市場）
    - summary: 100文字程度の短い要約。
    - details: 500文字程度の詳細な解説。

    {{
      "term": "{term}",
      "category_large": "...",
      "category_medium": "...",
      "category_small": "...",
      "summary": "...",
      "details": "..."
    }}
    """
    
    try:
        response = model.generate_content(system_prompt)
        # レスポンスからJSON部分を抽出
        json_response_str = response.text.strip().replace("```json", "").replace("```", "")
        json_response = json.loads(json_response_str)
        return json_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI response generation failed: {str(e)}")


@app.get("/api/history", response_model=List[schemas.History])
def read_all_histories(
    skip: int = 0, 
    limit: int = 100, 
    term: Optional[str] = None,
    category_large: Optional[str] = None,
    category_medium: Optional[str] = None,
    category_small: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """ 全ての履歴を取得する """
    histories = crud.get_all_histories(
        db, 
        skip=skip, 
        limit=limit,
        term=term,
        category_large=category_large,
        category_medium=category_medium,
        category_small=category_small,
        is_favorite=is_favorite
    )
    return histories

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    """ ユニークなカテゴリを取得する """
    return crud.get_unique_categories(db)

@app.get("/api/history/{history_id}", response_model=schemas.History)
def read_history(history_id: int, db: Session = Depends(get_db)):
    """ IDで単一の履歴を取得する """
    db_history = crud.get_history(db, history_id=history_id)
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return db_history

@app.delete("/api/history/{history_id}", response_model=schemas.History)
def delete_history_entry(history_id: int, db: Session = Depends(get_db)):
    """ IDで履歴を削除する """
    deleted_history = crud.delete_history(db, history_id=history_id)
    if deleted_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return deleted_history

@app.patch("/api/history/{history_id}/favorite", response_model=schemas.History)
def toggle_favorite_status(history_id: int, db: Session = Depends(get_db)):
    """ IDでお気に入り状態を切り替える """
    toggled_history = crud.toggle_favorite(db, history_id=history_id)
    if toggled_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return toggled_history

