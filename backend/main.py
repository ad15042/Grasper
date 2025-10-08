import os
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# リクエストボディの型定義
class UserInput(BaseModel):
    keyword: str

# Geminiモデルの準備
model = genai.GenerativeModel('gemini-2.5-pro')

@app.post("/api/generate")
async def generate_text(user_input: UserInput):
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
        # Geminiからのレスポンスは```json ... ```で囲まれていることがあるため、中身を抽出
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return {"data": cleaned_response}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "Backend is running."}
