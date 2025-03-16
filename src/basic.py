import os
import streamlit as st

if not os.getenv("CLOUD_RUN"): # ローカル実行の時のみ.envから環境変数を読む
    from dotenv import load_dotenv
    load_dotenv()

USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")

def check_credentials(username, password):
    """ユーザー名とパスワードが環境変数と一致するか確認します。"""
    return username == USERNAME and password == PASSWORD

def login():
    """ログインフォームを表示し、認証を行います。"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.get("authenticated"):
        return

    st.title("Basic認証")
    username = st.text_input("ユーザー名")
    password = st.text_input("パスワード", type="password")
    
    if st.button("ログイン"):
        if check_credentials(username, password):
            st.session_state.authenticated = True
            st.success("ログイン成功！")
            st.rerun()
        else:
            st.error("ユーザー名またはパスワードが間違っています。")
            st.session_state.authenticated = False
    
    st.stop()
