import streamlit as st
from src.basic import login
# from src.ip_auth import login
# from src.oauth import login

def main():
    # 認証
    login()

    # 認証済みの場合、メインアプリの画面を表示
    st.title("メインアプリ画面")
    st.write("ここにログイン後のアプリコンテンツを表示します。")

if __name__ == "__main__":
    main()
