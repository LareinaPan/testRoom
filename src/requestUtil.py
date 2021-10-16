import json
import pandas
import logging
from config.host import Host
from src.requestBassClass import requestBase
from src.tool.get_paths import GetPath,paths


def get_path(file_name, path_def="data/"):
    logging.info("同构文件名file_name和相对路径path_def获取绝对路径")
    paths = GetPath()
    file_path = paths.join_path(file_name, path=path_def)
    return file_path


def getValueIfNone(value, defaultValue):
    if value is not None:
        return value
    else:
        return defaultValue


def get_post_file_info(file_name, path_def=None, file_type=None, **kwargs):
    logging.info("入参文件名，相对路径")
    logging.info("kwargs: {'order_id':(None, 32480)}")
    files = {}
    if file_name:
        path_def_curr = getValueIfNone(path_def, "data/importfile")
        file_path = get_path(file_name, path_def_curr)
        if file_type is None:
            file_type = "sheet.sheet"
        files = {"file": (file_name, open(file_path, "rb"), file_type)}
    for keyName in kwargs.keys():
        tempData = {keyName: (None, kwargs[keyName])}
        files.update(tempData)
    return files

# 上传文件的接口
def post_file(url, file_name, path_def=None, file_type=None, **kwargs):
    urls = str(Host.BSAPI) + url
    files = get_post_file_info(file_name, path_def=path_def, file_type=file_type, **kwargs)
    res = requestBase.base_requests(urls, {}, content="web_upload_file", type="post_file", files=files)
    return res