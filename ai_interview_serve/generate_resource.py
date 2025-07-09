import requests


def call_dify_workflow_resource(knowledgePoints, user_id="user"):
    """
    调用 Dify 工作流的抽象函数
    """
    # Dify API 配置
    api_url = 'https://api.dify.ai/v1/workflows/run'
    api_key = 'app-XdlOzLvMjhNd8HVcXY5Tb9Pa'
    # 请求头
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # 请求参数
    payload = {
        "inputs": {
            'knowledgePoints': knowledgePoints,
        },
        "response_mode": "blocking",
        "user": user_id
    }

    try:
        # 发起请求
        response = requests.post(
            api_url,
            json=payload,
            headers=headers,
            timeout=60,
            proxies={
                "http": "http://127.0.0.1:7899",
                "https": "http://127.0.0.1:7899"
            }
        )
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception:
        return None
