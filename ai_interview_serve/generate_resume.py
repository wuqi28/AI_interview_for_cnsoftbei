# encoding: UTF-8
import time

import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
from PIL import Image
from io import BytesIO


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# 生成鉴权url
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


# 生成请求body体
def getBody(appid, text):
    body = {
        "header": {
            "app_id": appid,
            "status": 3,
        },
        "parameter": {
            "ai_resume": {
                "resData": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "reqData": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 3,
                "text": base64.b64encode(text.encode("utf-8")).decode('utf-8')
            }
        }
    }
    return body


# 发起请求并返回结果
def main(text, appid, apikey, apisecret):
    host = 'https://cn-huadong-1.xf-yun.com/v1/private/s73f4add9'
    url = assemble_ws_auth_url(host, method='POST', api_key=apikey, api_secret=apisecret)
    content = getBody(appid, text)
    # print(time.time())
    response = requests.post(url, json=content, headers={'content-type': "application/json"}).text
    # print(time.time())
    return response


def generate_resume_from_text(desc):
    # 运行前请配置以下鉴权三要素，获取途径：https://console.xfyun.cn/services/tti
    APPID = '11f5aa88'
    APISecret = 'Y2Y1NzA1OGE0NTE3ZDE4NTc0YzFkYTVm'
    APIKEY = '8fc04d9905f3dd62e31dcd3512073d9a'

    res = main(desc, appid=APPID, apikey=APIKEY, apisecret=APISecret)
    print(res)
    data = json.loads(res)
    code = data['header']['code']
    if (0 == code):
        text = data['payload']['resData']['text']
        resume = base64.b64decode(text)
        print("通过链接下降简历文件：", resume)
        return resume


if __name__ == '__main__':
    res = generate_resume_from_text("姓名：李四，年龄22，性别：男，电话：123456789000，目标岗位：AI人工智能算法工程师，技能特长：python、Java，flask、vue、数据结构、操作系统，教育背景：2025年毕业于清华大学，实习经历：2024年6月-2025年6月在科大讯飞实习，岗位：人工智能工程师")
    print(res)
