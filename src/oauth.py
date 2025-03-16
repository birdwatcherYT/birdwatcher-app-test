import streamlit as st
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import google.oauth2.id_token
import requests
import os
from secret import get_secret

if not os.getenv("CLOUD_RUN"): # ローカル実行の時のみ.envから環境変数を読む
    from dotenv import load_dotenv
    load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID")
OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")

client_config = {
    "web": {
        "client_id": get_secret(PROJECT_ID, OAUTH2_CLIENT_ID),
        "client_secret": get_secret(PROJECT_ID, OAUTH2_CLIENT_SECRET),
        "redirect_uris": [REDIRECT_URL],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

def get_google_flow():
    flow = Flow.from_client_config(
        client_config=client_config,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
        redirect_uri=client_config["web"]["redirect_uris"][0],
    )
    return flow

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.get("authenticated"):
        return

    # ログイン画面
    st.title("Google Sign-In")
    if "code" not in st.query_params:
        flow = get_google_flow()
        auth_url, _ = flow.authorization_url(prompt="consent")
        st.page_link(auth_url, label="Googleでログインする")
    else:
        code = st.query_params["code"]
        flow = get_google_flow()
        flow.fetch_token(code=code)
        credentials = flow.credentials

        request_session = requests.Session()
        token_request = google.auth.transport.requests.Request(session=request_session)
        try:
            id_info = google.oauth2.id_token.verify_oauth2_token(
                credentials.id_token, token_request, client_config["web"]["client_id"]
            )

            # たとえば、特定のメールドメインに限定したい場合は以下のようにチェックできます
            allowed_domains = ["example.jp"]
            user_email = id_info.get("email", "")
            if not any(user_email.endswith("@" + domain) for domain in allowed_domains):
                st.error("このアカウントではログインできません。")
                return

            # ここで認証されたユーザー情報（例：メールアドレスなど）を利用できます
            st.success(f"ログイン成功！ようこそ、{id_info.get('email')}さん")

            # 認証に成功したので、セッションステートに反映し画面を切り替え
            st.session_state["authenticated"] = True
            st.query_params.pop("code")
            st.rerun()
        except ValueError as e:
            st.error("トークンの検証に失敗しました。")
            st.error(e)

    st.stop()
