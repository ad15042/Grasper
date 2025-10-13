import os
import json
import google.generativeai as genai
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

# ローカルモジュールをインポート
import crud, models, schemas
from database import get_db

# 環境変数からAPIキーを読み込む
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# FastAPIアプリケーションの初期化
app = FastAPI()

# CORSミドルウェアの設定 (フロントエンドからのアクセスを許可)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 本番環境では特定のドメインに制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Geminiモデルの準備
model = genai.GenerativeModel('gemini-2.5-pro')

# --- Create ---
@app.post("/api/generate", response_model=schemas.History)
async def generate_text(user_input: schemas.HistoryCreate, db: Session = Depends(get_db)):
    """
    ユーザーからのキーワードを受け取り、Gemini APIで解説を生成する
    """
    keyword = user_input.keyword

    # --- ここでシステムプロンプトを制御します ---
    # AIに役割を与え、出力形式をJSONに指定する
    prompt = f"""
    あなたはITと創薬分野の専門家です。
    以下のキーワードについて、初心者にも分かりやすく、簡潔に解説してください。
    
    回答は必ず以下のJSON形式の回答だけを出力してください。
    他の形式での出力は認められません。
    {{
      "category": "このキーワードが最も関連するカテゴリ（例: 'IT', 'Web開発', '創薬', '分子生物学'など）",
      "summary": "100文字程度の簡単な要約",
      "details": "詳細な解説をマークダウン形式で記述"
    }}
    
    キーワード: {keyword}
    """
    
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        response_data = json.loads(cleaned_response)
        
        # DBに保存
        return crud.create_history(db=db, keyword=keyword, response_data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# --- Read (複数) ---
@app.get("/api/history", response_model=List[schemas.History])
def read_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    histories = crud.get_histories(db, skip=skip, limit=limit)
    return histories

# --- Read (単一) ---
@app.get("/api/history/{history_id}", response_model=schemas.History)
def read_history(history_id: int, db: Session = Depends(get_db)):
    db_history = crud.get_history(db, history_id=history_id)
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return db_history

# --- Delete ---
@app.delete("/api/history/{history_id}", response_model=schemas.History)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    db_history = crud.delete_history(db, history_id=history_id)
    if db_history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return db_history
