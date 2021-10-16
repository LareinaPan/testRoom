import logging
import configparser
from src.tool.get_paths import GetPath


class OpConfig:
    """
    读取ini配置文件中的参数值
    """

    def __init__(self, file, path_def="config/"):
        paths = GetPath()
        self.file_path = paths.join_path(file, path=path_def)
        logging.info("file_path={0}".format(self.file_path))
        self.cf = configparser.RawConfigParser()
        self.cf.read(self.file_path, encoding="utf-8-sig")


    def get_value(self, section, option):
        """
        :param section: 指定section
        :param option: 指定option
        :return: 返回对应的value
        """
        values = self.cf.get(section, option)
        logging.info("'读取到{0}下的{1}值：'".format(section, values))
        return values


    def updata_value(self, section, option, value):
        """
        :param section: 需要修改的select
        :param option: 需要修改的option
        :param value: 修改的新值
        :return:
        """
        self.cf.set(section, option, value)
        with open(self.file_path, "W+", encoding="utf-8-sig") as f:
            self.cf.write(f)

    def set_values_int(self, section, option):
        # 指定section中的选项强制转化为整数
        return self.cf.getint(section, option)


conf = OpConfig("worker.ini")


if __name__ == '__main__':
    kk = conf.get_value('cookies', 'PHPSESSID')
    print(kk, len(kk))
