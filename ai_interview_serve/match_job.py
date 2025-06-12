import requests
import os
import logging
import json

# 日志配置
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# 配置
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "app-VZWjISELiW56IX9b0qai00uq")
DIFY_WORKFLOW_ID = os.getenv("DIFY_WORKFLOW_ID", "IBagyZLpnhwuQinR")
DIFY_API_URL = f"https://api.dify.ai/v1/workflows/run"

USE_PROXY = os.getenv("USE_PROXY", "false").lower() == "true"
PROXIES = {
    "http": "http://127.0.0.1:7899",
    "https": "http://127.0.0.1:7899"
} if USE_PROXY else None

TIMEOUT = 30  # 请求超时时间（秒）


def run_dify_workflow(query: str, user_id="user") -> dict:
    """
    调用 Dify 工作流，传入岗位标签 query，返回推荐结果。

    参数:
        query (str): 岗位标签组合，例如 "前端开发工程师，web前端开发，数据标注"
        user_id (str): 可选，传入 user ID 用于区分调用方

    返回:
        dict: 包含 success 状态、data 或 error 的结果
    """
    if not query or not isinstance(query, str):
        return {"success": False, "error": "query 参数无效，必须是非空字符串"}

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {"query": query},
        "response_mode": "blocking",
        "user": user_id
    }

    try:
        logger.info(f"[Dify] 请求 URL: {DIFY_API_URL}")
        logger.info(f"[Dify] 请求 Payload: {json.dumps(payload, ensure_ascii=False)}")

        response = requests.post(
            DIFY_API_URL,
            headers=headers,
            json=payload,
            timeout=TIMEOUT,
            proxies=PROXIES
        )

        logger.info(f"[Dify] 响应状态码: {response.status_code}")

        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            logger.error(f"[Dify] 请求失败: {response.status_code}, 响应: {response.text}")
            return {
                "success": False,
                "error": f"状态码: {response.status_code}, 内容: {response.text}"
            }

    except requests.exceptions.Timeout:
        logger.error("[Dify] 请求超时")
        return {"success": False, "error": "请求超时"}
    except requests.exceptions.RequestException as e:
        logger.error(f"[Dify] 网络异常: {str(e)}")
        return {"success": False, "error": str(e)}
    except Exception as e:
        logger.error(f"[Dify] 未知错误: {str(e)}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    query = "前端开发工程师，web前端开发，数据标注，岗位标签"
    result = run_dify_workflow(query)

    if result['success']:
        raw_text = result['data']['data']['outputs']['text']  # 原始 JSON 字符串
        try:
            job_list = json.loads(raw_text)  # 转为 Python list
            jobs_json = json.dumps(job_list, indent=2, ensure_ascii=False)  # 格式化打印
            print(jobs_json)
        except json.JSONDecodeError as e:
            print("解析失败：", str(e))
            print("原始内容：", raw_text)
    else:
        print("调用失败：", result['error'])

