from fileupload import seve_file
import requests
import datetime
import hashlib
import base64
import hmac
import json
import os
import re
from pydub import AudioSegment


class get_result:
    def __init__(self, appid, apikey, apisecret):
        self.Host = "ost-api.xfyun.cn"
        self.RequestUriCreate = "/v2/ost/pro_create"
        self.RequestUriQuery = "/v2/ost/query"
        self.urlCreate = f"https://{self.Host}{self.RequestUriCreate}"
        self.urlQuery = f"https://{self.Host}{self.RequestUriQuery}"
        self.HttpMethod = "POST"
        self.APPID = appid
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"
        self.UserName = apikey
        self.Secret = apisecret
        self.Date = self.httpdate(datetime.datetime.utcnow())
        self.BusinessArgsCreate = {
            "language": "zh_cn",
            "accent": "mandarin",
            "domain": "pro_ost_ed"
        }

    def hashlib_256(self, res):
        m = hashlib.sha256(res.encode('utf-8')).digest()
        return "SHA-256=" + base64.b64encode(m).decode('utf-8')

    def httpdate(self, dt):
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest, uri):
        signature_str = f"host: {self.Host}\ndate: {self.Date}\n{self.HttpMethod} {uri} {self.HttpProto}\ndigest: {digest}"
        signature = hmac.new(self.Secret.encode('utf-8'),
                             signature_str.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature).decode('utf-8')

    def init_header(self, data, uri):
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest, uri)
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": f'api_key="{self.UserName}",algorithm="{self.Algorithm}", headers="host date request-line digest", signature="{sign}"'
        }

    def get_create_body(self, fileurl):
        return json.dumps({
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgsCreate,
            "data": {
                "audio_src": "http",
                "audio_url": fileurl,
                "encoding": "raw"
            }
        })

    def get_query_body(self, task_id):
        return json.dumps({
            "common": {"app_id": self.APPID},
            "business": {"task_id": task_id}
        })

    def call(self, url, body, headers):
        try:
            response = requests.post(url, data=body, headers=headers, timeout=8)
            return json.loads(response.text) if response.status_code == 200 else response.content
        except Exception as e:
            print("Exception:", e)

    def task_create(self, fileurl):
        body = self.get_create_body(fileurl)
        headers = self.init_header(body, self.RequestUriCreate)
        return self.call(self.urlCreate, body, headers)

    def task_query(self, task_id, fileurl):
        body = self.get_query_body(task_id)
        headers = self.init_header(self.get_create_body(fileurl), self.RequestUriQuery)
        return self.call(self.urlQuery, body, headers)

    def get_fileurl(self, file_path):
        api = seve_file.SeveFile(app_id=self.APPID, api_key=self.UserName, api_secret=self.Secret,
                                 upload_file_path=file_path)
        file_total_size = os.path.getsize(file_path)
        if file_total_size < 31457280:
            return api.gene_params('/upload')['data']['url']
        else:
            return api.gene_params('/mpupload/upload')

    def get_result(self, file_path):
        fileurl = self.get_fileurl(file_path)
        task_resp = self.task_create(fileurl)
        if not isinstance(task_resp, dict) or task_resp.get("code") != 0:
            print("创建任务失败:", task_resp)
            return task_resp

        task_id = task_resp['data']['task_id']
        print("任务转写中...")
        while True:
            result = self.task_query(task_id, fileurl)
            status = result.get("data", {}).get("task_status") if isinstance(result, dict) else None
            if status and status not in ('1', '2'):
                return result
            elif isinstance(result, bytes):
                return result


def parse_transcription_result(result: dict) -> str:
    if not result or "data" not in result:
        return ""
    lattice = result["data"].get("result", {}).get("lattice", [])
    return "".join(
        cw.get("w", "") for segment in lattice for rt in segment.get("json_1best", {}).get("st", {}).get("rt", []) for
        ws in rt.get("ws", []) for cw in ws.get("cw", []))


def convert_to_16k_16bit_mono(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.set_frame_rate(16000).set_channels(1).set_sample_width(2).export(output_path, format="wav")


def video_to_text(file_path):
    appid = "11f5aa88"
    apikey = "8fc04d9905f3dd62e31dcd3512073d9a"
    apisecret = "Y2Y1NzA1OGE0NTE3ZDE4NTc0YzFkYTVm"

    convert_to_16k_16bit_mono(file_path, file_path)
    xf = get_result(appid, apikey, apisecret)
    res = xf.get_result(file_path)
    return parse_transcription_result(res)



