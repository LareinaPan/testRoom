import json
import logging
import os
import re
import pandas
import yaml
import xlrd
from src.tool.get_paths import paths


def read_yaml(key):
    filepath = paths.join_path("parameters.yml", path="config/")
    fp = open(filepath, encoding='utf-8')
    testdata = yaml.load(fp, Loader=yaml.FullLoader)
    data = testdata[key]
    return data


def read_json(file_name):
    # 读取json格式数据，并返回list
    with open(file_name, 'r',encoding='utf8')as fp:
        json_data = json.load(fp)
        return json_data


def read_lastReport(reportPath, reportName=''):
    """
    对目录下的文件按照时间排序，取日期最新的测试报告返回
    :param reportPath: 测试报告存放目录
    :param reportName: 按报告名称筛选，不传默认返回最新
    :return: 返回最新的测试文件
    """
    print("reportPath==>", reportPath)
    print("reportName==>", reportName)
    lists = os.listdir(reportPath) # 获取目录下的所有文件和文件夹

    new_dir = []

    if reportName != '':
        for filepath in lists:
            if re.match(reportName, filepath): # 报告开头的名称reportName
                new_dir.append(filepath)
    else:
        new_dir = lists

    # os.path.getctime 按文件创建时间升序排，getmtime[修改时间]
    new_dir.sort(key=lambda fn: os.path.getctime(reportPath + '\\' + fn), reverse=False)
    print("new_dir==>", new_dir)
    file_new = os.path.join(reportPath, new_dir[-1])
    return file_new


def read_excel(dir, index=0):
    """
    xlrd.open_workbook 打开excel
    sheets()#读取所有sheet表
    sheets[index] #读取指定工作表
    nrows:所有行数
    col_values(i) # 读取指定列的所有数据
    row_values(i) # 读取指定行的所有数据
    cell_values(1,1) # 读取单元格数据
    :param dir:
    :param index:
    :return:
    """
    book = xlrd.open_workbook(filename=dir)
    sheets = book.sheets()
    sheet = sheets[index]
    return sheet


def csv_to_dict(file, path='data/'):
    """
    读取csv中数据
    :param file:
    :param path:
    :return:
    """
    filename = paths.join_path(file, path)
    data_list = read_csv(filename)
    keys = data_list[0]
    res = data_list[1:]
    zip_list = []
    for i in res:
        zip_data = dict(zip(keys, i))
        field2s = zip_data["name"]
        field2s_list = []

    if field2s == '':
        pass
    else:
        if ';' in field2s:
            f = field2s.split(';')
            for aa in f:
                field2s_list.append(aa)
        else:
            field2s_list.append(field2s)
    zip_data["name"] = field2s_list
    zip_list.append(zip_data)
    print("scv数据拼接后的数据 ==>", zip_list)
    logging.info("scv数据拼接后的数据 ==>", zip_list)
    return zip_list


def read_csv(filename):
    """
    读取csv中数据
    :param filename: 文件的绝对路径
    :return: 每一行数据以list形式返回
    """
    with open(filename, encoding="utf-8")as file:
        data_list = []
        for line in file:
            data = line.split('\n')[0].split(',')
            data_list.append(data)
        logging.info("csv中数据凭借后的数据 ==>", data_list)
        return data_list


if __name__ == "__main__":
    base_url = csv_to_dict('my.csv')
    print(base_url)

