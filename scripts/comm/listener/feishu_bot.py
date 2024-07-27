import json
import requests

from comm.listener.listener import Listener
from comm.event import Event


class FeishuBot(Listener):
    def notify(self, e: Event):
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {"receive_id_type": "open_id"}
        msgContent = {
            "text": e.message,
        }
        req = {
            "receive_id": "ou_787f4014258340eae32d5c00ebabaca5",
            "msg_type": "text",
            "content": json.dumps(msgContent)
        }
        payload = json.dumps(req)
        headers = {
            "Authorization": "Bearer t-g1047rf7HEPEO6QVWPJFB25TV6EIML3RSSQP22PU",
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, params=params, headers=headers, data=payload
        )
        print(response.headers['X-Tt-Logid'])
        print(response.content)
