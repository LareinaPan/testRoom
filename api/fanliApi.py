from data.fanliData import *
from config import host
from importlib import reload
import requests
from src.requestBassClass import requestBase
from src.requestUtil import *


reload(host)
Host = host.Host


def get_ajaxZhideCatItems(**kwargs):
    url = str(Host.fun) + '/homepage/ajaxZhideCatItems'
    data = jquery
    data.update(**kwargs)
    res = requestBase.base_requests(url, data)
    return res


def post_op_wx_back_qrcode_upload(**kwargs):
    """
    上传文件接口示例
    :param kwargs:
    :return:
    """
    currUrl = '/homepage/ajaxZhideCatItems/upload'
    data = jquery
    file_name = kwargs["file_name"]
    kwargs.pop("file_name")
    file_type = "image/jpeg"
    res = post_file(currUrl, file_name, file_type=file_type, **data)
    return res


# if __name__ == "__main__":
#     tt = get_ajaxZhideCatItems()
#     print(tt.status_code)