# -*- coding: utf-8 -*-
# @Time    : 12/5/22 9:54 PM
# @FileName: __init__.py
# @Software: PyCharm
# @Github    ：sudoskys
import os
import json
from .network import request


def _load_api():
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), ".", "api_url.json")
    )
    if os.path.exists(path):
        with open(path, encoding="utf8") as f:
            return json.loads(f.read())
    else:
        raise FileNotFoundError("NotFind:api_url.json")


API = _load_api()


class Completion(object):
    def __init__(self, api_key: str, proxy_url: str = ""):
        self.__api_key = api_key
        self.__proxy = proxy_url

    def get_api_key(self):
        return self.__api_key

    async def create(self, model: str = "text-davinci-003",
                     prompt: str = "Say this is a test",
                     temperature: float = 0,
                     max_tokens: int = 7,
                     **kwargs
                     ):
        """
        得到一个对话，预设了一些参数，其实还有很多参数，如果你有api文档
        :param model: 模型
        :param prompt: 提示
        :param temperature: unknown
        :param max_tokens: 返回数量
        :return:
        """
        """
        curl https://api.openai.com/v1/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer YOUR_API_KEY" \
        -d '{"model": "text-davinci-003", "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7}'
        """
        api = API["v1"]["completions"]
        # 参数决定
        params = {"model": model,
                  "prompt": prompt,
                  "temperature": temperature,
                  "max_tokens": max_tokens
                  }
        api_config = {param: api["params"][param]["Defaults"]
                      for param in api["params"].keys()
                      if (param in kwargs) or (param in params)
                      }
        api_config.update(params)
        api_config.update(kwargs)
        # 返回请求
        return await request("POST",
                             api["url"],
                             data=api_config,
                             auth=self.__api_key,
                             proxy=self.__proxy,
                             json_body=True,
                             )
