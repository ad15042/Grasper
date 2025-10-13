# ベースとなる公式Pythonイメージを指定
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリの定義ファイルを先にコピー
COPY requirements.txt .

# ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードを全てコピー
COPY . .

# ENTRYPOINT [ "./entrypoint.sh " ]

# コンテナ起動時にUvicornでFastAPIサーバーを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
