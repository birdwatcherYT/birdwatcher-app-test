import streamlit as st
from flask import Flask, request
import threading

# Flask アプリケーション
app = Flask(__name__)

# Flaskのエンドポイントで、X-Forwarded-For ヘッダーから IP アドレスを取得
@app.route('/get_ip')
def get_ip():
    forwarded_for = request.headers.get('X-Forwarded-For', 'X-Forwarded-For ヘッダーが見つかりません')
    return forwarded_for

# Streamlitアプリケーション
st.title("IPアドレス確認")

# Flask サーバーをバックグラウンドで起動
def start_flask():
    app.run(host="0.0.0.0", port=5000)

flask_thread = threading.Thread(target=start_flask)
flask_thread.daemon = True
flask_thread.start()

# Flask サーバーから IP アドレスを取得する
import requests

# Render や Cloud Run にデプロイされている場合、このURLにリクエストを送る
flask_ip_url = "http://127.0.0.1:5000/get_ip"

try:
    response = requests.get(flask_ip_url)
    ip_address = response.text
    st.write(f"X-Forwarded-For ヘッダーから取得したIPアドレス: {ip_address}")
except requests.exceptions.RequestException as e:
    st.write(f"Flaskサーバーへのリクエストに失敗しました: {e}")

st.write("Streamlit アプリで `X-Forwarded-For` ヘッダーから IP アドレスを取得しています。")
