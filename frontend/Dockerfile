# ベースとなる公式Node.jsイメージを指定
FROM node:20-alpine

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のファイルを先にコピーして、キャッシュを有効活用
COPY package*.json ./

# 依存ライブラリをインストール
RUN npm install

# アプリケーションのソースコードを全てコピー
COPY . .

# Next.jsアプリのデフォルトポートを開放
EXPOSE 3000

# コンテナ起動時に実行する開発サーバー起動コマンド
CMD ["npm", "run", "dev"]