import streamlit as st
from streamlit_javascript import st_javascript

def get_client_ip():
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
        pass
    return None

ip_address = get_client_ip()
if ip_address:
    st.write(f"クライアントIPアドレス: {ip_address}")
else:
    st.write("クライアントIPアドレスを取得できませんでした。")

def get_client_ip_render():
    ip_address = st.context.headers.get("X-Forwarded-For")
    if ip_address:
        return ip_address.split(',')
    return None

ip_address2 = get_client_ip_render()
if ip_address2:
    st.write(f"クライアントIPアドレス: {ip_address2}")
else:
    st.write("クライアントIPアドレスを取得できませんでした。")
