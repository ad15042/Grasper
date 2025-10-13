# Grasper 🧠

Grasperは、GoogleのGemini APIを活用して、ユーザーが入力したキーワードに関する情報を生成・永続化するWebアプリケーションです。

生成された内容はPostgreSQLデータベースに保存され、いつでも閲覧・管理が可能です。これにより、AIとの対話を通じて、あなただけの再利用可能なナレッジベースを構築できます。



---

## ✨ 主な機能

-   **AIによる解説生成**: 入力されたキーワードに基づき、Gemini APIがリアルタイムで解説文を生成します。
-   **生成履歴の永続化**: 生成されたキーワード、カテゴリ、要約、詳細解説はすべてPostgreSQLデータベースに保存されます。
-   **インタラクティブな履歴管理**:
    -   **一覧表示**: 保存された履歴をサイドバーに一覧表示します。
    -   **詳細表示**: 履歴項目をクリックすると、過去の生成内容をメイン画面で確認できます。
    -   **削除機能**: 不要になった履歴はボタン一つで簡単に削除できます。
-   **AlembicによるDBスキーマ管理**: データベースのテーブル構造の変更をバージョン管理し、安全なマイグレーションを実現します。
-   **モダンなUI**: ReactとTailwind CSSによる、シンプルで洗練されたシングルページアプリケーションです。
-   **Docker化された開発環境**: Docker Composeにより、コマンド一つでバックエンド、フロントエンド、データベースを含む完全な開発環境を構築・起動できます。

---

## 💻 技術スタック

このプロジェクトは、以下の技術を使用して構築されています。

-   **フロントエンド**: HTML / React (CDN) / Tailwind CSS (CDN)
-   **バックエンド**: Python / **FastAPI**
-   **データベース**: **PostgreSQL**
-   **ORM**: **SQLAlchemy**
-   **DBマイグレーション**: **Alembic**
-   **AIモデル**: Google Gemini API
-   **Webサーバー**: Nginx (フロントエンド配信用)
-   **コンテナ技術**: Docker / Docker Compose

---

## 🚀 セットアップと実行方法

### 1. 前提条件

-   [Docker](https://www.docker.com/get-started) と [Docker Compose](https://docs.docker.com/compose/install/) がインストールされていること。
-   [Git](https://git-scm.com/) がインストールされていること。
-   Google Gemini APIキーを取得していること。([Google AI for Developers](https://ai.google.dev/)から取得できます)

### 2. インストール

まず、このリポジトリをクローンします。

```bash
git clone [https://github.com/your-username/my-gemini-app.git](https://github.com/your-username/my-gemini-app.git)
cd my-gemini-app
```

### 3. 環境変数の設定
プロジェクトのルートディレクトリに `.env` という名前のファイルを作成し、ご自身のGemini APIキーとデータベース接続情報を設定します。ローカルでの開発の場合、APIキー以外は下記の内容のままで問題ありません。
```ini
# .envファイル

# ご自身のAPIキーに書き換えてください
GEMINI_API_KEY="YOUR_API_KEY_HERE"

# PostgreSQL Settings
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword

# Database URL for FastAPI application
DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydb
```

### 4. アプリケーションの起動

以下のコマンドを実行して、Dockerコンテナをビルドし、バックグラウンドで起動します。
以下のコマンドを実行して、Dockerコンテナをビルドし、バックグラウンドで起動します。
このコマンドは、コンテナの起動時に`entrypoint.sh`を通じてデータベースのマイグレーションも自動的に実行します。

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



## 📁 プロジェクト構成

```plaintext
/my-gemini-app/
├── .env                  # 環境変数
├── docker-compose.yml    # Dockerコンテナ構成定義
|
├── backend/              # FastAPIバックエンド
│   ├── alembic/          # Alembicマイグレーションスクリプト
│   ├── alembic.ini       # Alembic設定
│   ├── Dockerfile
│   ├── entrypoint.sh     # コンテナ起動時スクリプト
│   ├── database.py       # DB接続設定
│   ├── models.py         # DBテーブル(モデル)定義
│   ├── schemas.py        # APIデータ型(スキーマ)定義
│   ├── crud.py           # DB操作(CRUD)ロジック
│   ├── requirements.txt
│   └── main.py           # APIエンドポイント定義
│
└── frontend/             # 静的フロントエンド
    └── index.html
```