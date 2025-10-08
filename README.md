# Grasper 🧠

Grasperは、GoogleのGemini APIを活用して、ユーザーが入力したキーワードに関する情報を生成・表示するシンプルなWebアプリケーションです。

モダンなUIでAIからの回答をインタラクティブに取得し、自分だけのナレッジベースを構築する第一歩となります。



---

## ✨ 主な機能

- **AIによる解説生成**: 入力されたキーワードに基づき、Gemini APIがリアルタイムで解説文を生成します。
- **構造化されたレスポンス**: AIからの回答は「カテゴリ」「要約」「詳細」を含むJSON形式で整形されるため、将来的なデータ活用が容易です。
- **モダンなUI**: ReactとTailwind CSSによる、シンプルで洗練されたシングルページアプリケーションです。
- **Docker化された環境**: Docker Composeにより、コマンド一つで開発環境を簡単に構築・起動できます。

---

## 💻 技術スタック

このプロジェクトは、以下の技術を使用して構築されています。

- **フロントエンド**: HTML / React (CDN) / Tailwind CSS (CDN)
- **バックエンド**: Python / FastAPI
- **AIモデル**: Google Gemini API
- **Webサーバー**: Nginx (フロントエンド配信用)
- **コンテナ技術**: Docker / Docker Compose

---

## 🚀 セットアップと実行方法

### 1. 前提条件

- [Docker](https://www.docker.com/get-started) と [Docker Compose](https://docs.docker.com/compose/install/) がインストールされていること。
- [Git](https://git-scm.com/) がインストールされていること。
- Google Gemini APIキーを取得していること。([Google AI for Developers](https://ai.google.dev/)から取得できます)

### 2. インストール

まず、このリポジトリをクローンします。

```bash
git clone [https://github.com/your-username/my-gemini-app.git](https://github.com/your-username/my-gemini-app.git)
cd my-gemini-app
```

### 3. 環境変数の設定

プロジェクトのルートディレクトリに `.env` という名前のファイルを作成し、ご自身のGemini APIキーを設定します。

```.env:.env
# .envファイル

# ご自身のAPIキーに書き換えてください
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4. アプリケーションの起動

以下のコマンドを実行して、Dockerコンテナをビルドし、バックグラウンドで起動します。

```bash
docker-compose up --build -d
```

### 5. アプリケーションへのアクセス

コンテナの起動後、Webブラウザで以下のURLにアクセスしてください。

- **フロントエンド**: `http://localhost:3000`

アプリケーションが正常に表示されれば、セットアップは完了です！

### 6. アプリケーションの停止

アプリケーションを停止する場合は、以下のコマンドを実行します。

```bash
docker-compose down
```

---

## 📁 プロジェクト構成

```plaintext
/my-gemini-app/
├── .env                  # 環境変数（APIキーなど）
├── docker-compose.yml    # Dockerコンテナの構成定義
|
├── backend/              # FastAPIバックエンド
│   ├── Dockerfile
│   ├── requirements.txt
│   └── main.py
│
└── frontend/             # 静的フロントエンド
    └── index.html
```