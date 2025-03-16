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

SecretManagerへのアクセスはoauth.pyからのみ行っています。  
必要に応じてBASIC認証のパスワードもSecretManagerに登録するなどしてください。  
Render等のGoogle外サービスへデプロイする際で、アクセスが難しいときは、環境変数にパスワードを記載し、get_secret関数を外してください。


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

## デプロイ
### CloudRun
Google認証を使う場合
```sh
gcloud run deploy streamlit-app-test --region "us-central1" --source . \
  --set-env-vars PROJECT_ID=プロジェクトID,OAUTH2_CLIENT_ID=oauth2-client-id,OAUTH2_CLIENT_SECRET=oauth2-client-secret,REDIRECT_URL=デプロイ後に生成されるURLを入れる \
  --max-instances 2
```
- 使う認証方法に応じて環境変数を変えてください

### AppEngine
```sh
gcloud app deploy
```
- `app.yaml`を適切に書き換えてから実行
