import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_javascript import st_javascript

# ローカル用
load_dotenv()

IP_ADDRESSES = os.environ.get("IP_ADDRESSES", "").split(",")

def get_client_ip_by_api():
     url = 'https://api.ipify.org?format=json'
     script = (
         f'await fetch("{url}").then('
         'function(response) {'
         'return response.json();'
         '})'
     )
     try:
         result = st_javascript(script)
         if isinstance(result, dict) and 'ip' in result:
             return result['ip']
     except:
        return ""
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
    if ip_address is None:
        st.write("IPアドレス確認中...")
    elif ip_address in IP_ADDRESSES:
        st.write(f"クライアントIPアドレス: {ip_address}")
        st.success("ログイン成功！")
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.write(f"クライアントIPアドレス: {ip_address}")
        st.error("許可されていないIPアドレスです")
        st.session_state.authenticated = False

    st.stop()


