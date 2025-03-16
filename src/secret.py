from google.cloud import secretmanager

def get_secret(project_id, secret_id, version_id="latest"):
    """Secret Managerからパスワードを取得する
    
    Args:
      project_id (str): Google Cloud プロジェクト ID
      secret_id (str): シークレットの ID
      version_id (str): シークレットのバージョン (デフォルトは "latest")
    """
    # クライアントの初期化
    client = secretmanager.SecretManagerServiceClient()
    # シークレットのパスを作成
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    # シークレットのアクセス
    response = client.access_secret_version(name=name)
    # ペイロードの取得
    payload = response.payload.data.decode("UTF-8")

    return payload
