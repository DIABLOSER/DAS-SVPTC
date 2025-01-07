# douyin_api.py

from douyin_config import DOUYIN_API, DOUYIN_CLIENT_KEY, DOUYIN_CLIENT_SECRET
import requests
import json

class Config:
    def __init__(self):
        self.client_key = DOUYIN_CLIENT_KEY
        self.client_secret = DOUYIN_CLIENT_SECRET

class ItemBaseRequest:
    def __init__(self, access_token, item_id, open_id):
        self.access_token = access_token
        self.item_id = item_id
        self.open_id = open_id

class Client:
    def __init__(self, config):
        self.config = config
        self.base_url = DOUYIN_API

    def make_request(self, method, endpoint, headers=None, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = headers or {}
        headers["Content-Type"] = "application/json"
        if self.config.client_key and self.config.client_secret:
            headers["Authorization"] = f"Bearer {self.config.client_key}:{self.config.client_secret}"
        
        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

    def item_base(self, request):
        headers = {
            "Authorization": f"Bearer {request.access_token}"
        }
        data = {
            "item_id": request.item_id,
            "open_id": request.open_id
        }
        return self.make_request("POST", "item/base/", headers=headers, data=data)

def get_item_base_info(access_token, item_id, open_id):
    """
    获取商品基础信息

    :param access_token: 访问令牌
    :param item_id: 商品ID
    :param open_id: 开放ID
    :return: 商品基础信息的 JSON 响应
    """
    config = Config()
    client = Client(config)
    request = ItemBaseRequest(access_token, item_id, open_id)
    return client.item_base(request)