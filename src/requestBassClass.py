import time
import requests
import json
import logging

from src.tool.opFileData import read_yaml
from src.tool.op_config import OpConfig


class RequestsBase:

    @classmethod
    def base_requests(cls, url, data, types='get', content='text', json_data="", files=None, appcookie=None):
        """
        用于工单系统的接口调用
        :param data: 入参为json[application/json]
        :param types: 请求的方法
        :param content: 请求的参数格式
        :param url: host
        :return: 接口返回的json格式数据content-Type
        """
        conf = OpConfig('worker.ini')
        cookies = conf.get_value("cookies", "PHPSESSID")

        if content == "json":
            headers = requestBase.jsonHeaders("PHPSESSID", cookies)
        elif content == "text":
            headers = requestBase.textHeaders()
        else:
            raise IOError("接口请求数据不正常")

        currCookie = headers.get("cookie")
        logging.info("当前请求的cookie值{}".format(currCookie))

        try:
            if types == 'post':
                res = requests.post(url=url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"), headers=headers, verify=False)
            elif types == 'get':
                res = requests.get(url=url, params=data, headers=headers, verify=False)
            elif types == 'post_pararms':
                res = requests.post(url=url, params=data, headers=headers, verify=False)
            elif types == 'post_json':
                res = requests.post(url=url, params=data, json=json_data, headers=headers, verify=False)
            elif types == 'export':
                res = requests.get(url=url, params=data, headers=headers, verify=False, stream=False)
            elif types == 'post_file':
                res = requests.post(url=url, params=data, headers=headers, verify=False)
            elif types == 'put':
                res = requests.put(url=url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"), headers=headers, verify=False)
            elif types == 'delete':
                res = requests.delete(url=url, data=json.dumps(data, ensure_ascii=False).encode("utf-8"), headers=headers, verify=False)

            logging.info("请求体数据url:{}".format(res.request.url))

            if types == "post_file":
                logging.info("请求体数据body:{}".format(files))
            else:
                logging.info("请求体数据body:{}".format(data))

            if types == "export":
                logging.info("返回数据body:{}".format(res.content))
            else:
                res_body = res.content.decode("utf-8")
                logging.info("返回数据body:{}".format(res.body))

        except Exception as e:
            logging.info("调用接口失败==>{}".format(e))
            print("调用接口失败==>{}".format(e))
            return 0
        else:
            if content == "excel":
                return res
            else:
                return res.json()

    @staticmethod
    def readUrl(key):
        """
        获取yaml文件中的url
        :return:返回baseurl下的key值
        """
        base_url = read_yaml('base_url')[key]
        return base_url


    def jsonHeaders(self, **cookies):
        """
        :param cookies:传参一定要传key_value,不能只传一个参数
        :return:
        """
        headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
            "content-Type": "application/json",
            "Accept": "*/*"
        }
        if cookies:
            if len(cookies) == 2:
                headers["cookie"] = str(cookies[0]) + "=" + str(cookies[1])
        return headers

    def textHeaders(self, **cookies):
        """
        :param cookies:传参一定要传key_value,不能只传一个参数
        :return:
        """
        headers = {
            "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
            "content-Type": "text/html; charset=utf-8",
            "Accept": "*/*",
            "cookie": "FirstUrl=https%3A//www.baidu.com/link%3Furl%3DS_327dnYoIveQ-KWn8CBaXSfg_mPVvwIFiQcSnsTtHW%26wd%3D%26eqid%3Df84e0b72001a2c2400000002615a700c; LandingUrl=https%3A//www.fanli.com/; __utmv=95269DEF-1D90-4828-9D62-FA52E2E9A27F; __utmo=1225544299.575544229.3718452414; __utmp=1225544299.575544229.2652767557; UM_distinctid=17c4945e0a2ada-0c2a119a221a73-b7a1a38-e1000-17c4945e0a3b1b; PHPSESSID=hezwsraw8dz9w28yk8ehek0zbl; LOGERRTIMES=0; Hm_lvt_545c20cb01a15219bfeb0d1f103f99c1=1633496744,1633497389,1633499745,1633503521; c=xjZGRKOJ-1633503627904-18198c5ea4fb5215532876; TDpx=0; _fmdata=sZMEnCNYGuHAg23yOaKXCX22L7wKa8KoLQ3YIr3OPD8%2BZ4%2FIZNe9OLKOCDfjx6D6PadAUpr0m9v9BOSia%2Frz9r%2Fvw1sgxR4KDemc59SUayQ%3D; regurl=https%3A%2F%2Fpassport.fanli.com%2Freg%3Faction%3Dyes%26go_url%3Dhttps%253A%252F%252Fwww.fanli.com%252F; _xid=hAXoqJVL%2F6bZlhM4%2B06lRAfgtgVdgVzgM0MA78tc8zU4zSDWrZPc7qWsvTZBXCORJfBrt0mSnn8dVlMZnMWpgg%3D%3D; prouserid=474761424; prousername=1300212822720211006846; prousernameutf=1300212822720211006846; loginverify=77776d9f91dca7c9; prolong=1633503688; Hm_lpvt_545c20cb01a15219bfeb0d1f103f99c1=1633503693; lngmsgcnt=9; __fl_trace_cpc=D4E3D308-3F8F-4EC8-8A50-3CEF3C357612"
        }
        headers.update(**cookies)
        return headers

requestBase = RequestsBase()

# if __name__ == "__main__":
#     baseUrl = requestBase.base_requests(url, data)
#     print(baseUrl)
