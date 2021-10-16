import time
import datetime
from src.tool.get_paths import paths
from src.tool.op_config import OpConfig

"""
返回各种时间类型的处理脚本
"""


# 获取当前时间戳，并加上diet,单位ms，diet是秒
class getTime():
    now = datetime.datetime.now() # 获取当前日期
    delta = datetime.timedelta(days=7) #时间相差7天
    deltaOne = datetime.timedelta(days=1)
    delta30 = datetime.timedelta(days=30)

    @staticmethod
    def unixtime():
        # 获取当前时间戳
        unixtime = time.time()
        return int(unixtime)

    @staticmethod
    def str_time():
        """
        :return: 格式 2021-10-08 14:58:54
        """
        strTime = getTime.now.strftime('%Y-%m-%d %H:%M:%S')
        return strTime


    @staticmethod
    def str_data_before():
        """
        :return: 格式 2021-10-08,当前日期前一天
        """
        strBeforetime = (getTime.now - getTime.deltaOne).strftime('%Y-%m-%d')
        return strBeforetime


    @staticmethod
    def str_Ctime():
        """
        :return: 格式 2021-10-08 ,当日0点
        """
        now = datetime.datetime.now()
        zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute,
                                              seconds=now.second, microseconds=now.microsecond)
        strTime = zero_today.strftime('%Y-%m-%d %H:%M:%S')
        return strTime


    @staticmethod
    def str_time_before():
        """
        :return: 当前日期7天前
        """
        strBeforetime = (getTime.now - getTime.delta).strftime('%Y-%m-%d %H:%M:%S')
        return strBeforetime


    @staticmethod
    def str_time_after():
        """
        :return: 当前日期7天后
        """
        strAftertime = (getTime.now + getTime.delta).strftime('%Y-%m-%d %H:%M:%S')
        return strAftertime


    @staticmethod
    def unixtime_end():
        """
        :return: 当前日期30天后的时间戳
        """
        today = datetime.datetime.now()
        t2 = (today + datetime.timedelta(days=30)).strftime('%Y-%m-%d 00:00:00')

        # 转为秒级时间戳
        end_time = time.mktime(time.strptime(t2, '%Y-%m-%d %H:%M:%S'))
        str_time = str(end_time).split(".")[0] # 秒时间戳
        str_time2 = str(end_time * 1000).split(".")[0] # 转为毫秒级


        return str_time2


getTimeClass = getTime()
if __name__ == "__main__":
    te = getTimeClass.unixtime_end()
    print(te)
