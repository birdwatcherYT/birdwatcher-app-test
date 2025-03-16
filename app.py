import streamlit as st
import os
import requests

# 外部API (https://api.ipify.org) からIPアドレスを取得する関数
def get_ipify_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_address = response.json()['ip']
        return ip_address
    except requests.exceptions.RequestException as e:
        return f"IPify APIの取得に失敗: {e}"

# 環境変数 'HTTP_X_FORWARDED_FOR' からIPアドレスを取得する関数
def get_env_ip():
    forwarded_for = os.getenv('HTTP_X_FORWARDED_FOR', None)
    if forwarded_for:
        ip_address = forwarded_for.split(',')[0]
        return ip_address
    return 'HTTP_X_FORWARDED_FOR ヘッダーが見つかりません'

# Streamlitアプリケーション
st.title("IPアドレス確認のテスト")

# それぞれの取得方法を実行
ipify_ip = get_ipify_ip()
env_ip = get_env_ip()

# クラウド環境でX-Forwarded-For ヘッダーが正しく取得されることを確認する
# ここでは環境変数 HTTP_X_FORWARDED_FOR に格納されるIPアドレスを取得する

st.write(f"IPify API から取得したIPアドレス: {ipify_ip}")
st.write(f"環境変数 'HTTP_X_FORWARDED_FOR' から取得したIPアドレス: {env_ip}")
