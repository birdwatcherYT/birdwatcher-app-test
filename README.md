# streamlitアプリ認証テスト

## 構成
- `app.py`: streamlitメインアプリ（好きな認証を呼び出して）
- `src/`
    - `basic.py`: BASIC認証
    - `ip_auth.py`: IPアドレス認証
    - `oauth.py`: Google認証(example.jpだけを許す)
    - `secret.py`: SecretManagerへのアクセス関数
- `app.yaml`: AppEngineデプロイ用設定ファイル
- `Dockerfile`: CloudRun/AppEngineデプロイ用Dockerfile
- `requirements.txt`: Renderデプロイ用ファイル
- `uv.lock`, `pyproject.toml`: パッケージ管理

## ローカルテスト
- `uv sync`
- `uv run streamlit run app.py`

ローカル用 `.env`
```
# BASIC認証
BASIC_AUTH_USERNAME="ユーザー名"
BASIC_AUTH_PASSWORD="パスワード"

# IPアドレスチェック
IP_ADDRESSES="IPアドレス1,IPアドレス2,..."

# OAuth2.0
PROJECT_ID="プロジェクトID"
OAUTH2_CLIENT_ID="oauth2-client-id"
OAUTH2_CLIENT_SECRET="oauth2-client-secret"
REDIRECT_URL="http://localhost:8501"
```
