import streamlit as st
import os
import requests

if not os.getenv("CLOUD_RUN"): # ローカル実行の時のみ.envから環境変数を読む
    from dotenv import load_dotenv
    load_dotenv()

IP_ADDRESSES = os.environ.get("IP_ADDRESSES", "").split(",")

def get_client_ip_by_api():
    url = 'https://api.ipify.org?format=json'
    try:
        response = requests.get(url)
        result = response.json()
        if 'ip' in result:
            return result['ip']
    except Exception as e:
        print(f"Error occurred: {e}")
    return None

def get_client_ip_by_header():
    # ローカルでは動作確認できないので使っていない
    ip_address = st.context.headers.get("X-Forwarded-For")
    if ip_address:
        return ip_address.split(',')[0].strip()
    return None

def login():
    """IP認証"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if st.session_state.get("authenticated"):
        return

    st.title("IP認証")
    ip_address = get_client_ip_by_api()
    # ip_address = get_client_ip_by_header()
    if ip_address in IP_ADDRESSES:
        st.write(f"クライアントIPアドレス: {ip_address}")
        st.success("ログイン成功！")
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.error("許可されていないIPアドレスです")
        st.session_state.authenticated = False

    st.stop()


