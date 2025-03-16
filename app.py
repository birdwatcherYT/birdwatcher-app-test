import streamlit as st
import requests

# 外部API (https://api.ipify.org) からIPアドレスを取得する関数
def get_ipify_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_address = response.json()['ip']
        return ip_address
    except requests.exceptions.RequestException as e:
        return f"IPify APIの取得に失敗: {e}"

# X-Forwarded-For ヘッダーからIPアドレスを取得する関数
def get_forwarded_for_ip():
    # Render などでは `X-Forwarded-For` がリクエストヘッダーに含まれる
    forwarded_for = st.experimental_get_query_params().get('X-Forwarded-For', [None])[0]
    # forwarded_for = st.query_params.get('X-Forwarded-For', [None])[0]
    if forwarded_for:
        return forwarded_for.split(',')[0]  # 最初のIPアドレスを返す
    return 'X-Forwarded-For ヘッダーが見つかりません'

# Streamlitアプリケーション
st.title("IPアドレス確認のテスト")

# それぞれの取得方法を実行
ipify_ip = get_ipify_ip()
forwarded_for_ip = get_forwarded_for_ip()

st.write(f"IPify API から取得したIPアドレス: {ipify_ip}")
st.write(f"X-Forwarded-For ヘッダーから取得したIPアドレス: {forwarded_for_ip}")
