import os
import logging
"""
传入项目中的文件名，返回文件的绝对路径
"""


class GetPath:
    def get_path(self, path, root_path="projectPytest"):
        """
        :files :项目名称
        :param path: 当前文件的绝对路径
        :param root_path: 项目名称
        :return: 返回当前工程的路径，用于文件存储时拼接绝对路径，
        调用后，使用join来拼接C文件名+.py的绝对路径
        """
        dirc = os.path.dirname(path)
        path_split = os.path.split(dirc)
        if path_split[1] == root_path:
            return dirc
        else:
            return self.get_path(dirc)

    def join_path(self, files, path="config/"):
        """
        :param files: 文件名
        :param path: 项目下的一级目录，也可转入config/data
        :return:
        """
        ls_path = os.path.abspath(__file__)
        data = ls_path.split("src")
        logging.info("当前文件的位置：{}".format(ls_path))
        file = path+files
        filepath = os.path.join(data[0], file) # 动态文件的绝对路径
        logging.info("配置文件路径.{}".format(filepath))
        return filepath


    def join_path2(self, files, path="config/"):
        """
        :param files: 文件名
        :param path: 项目下的一级目录，也可转入config/data
        :return:
        """
        ls_path = os.path.abspath(__file__)
        logging.info("当前文件的位置：{}".format(ls_path))
        path_data = self.get_path(ls_path)
        file = path+files
        filepath = os.path.join(path_data, file) # 动态文件的绝对路径
        logging.info("配置文件路径.{}".format(filepath))
        return filepath


paths = GetPath()


if __name__ =="__main__":
    p = GetPath()
    # yy = p.get_path("D:/projectPytest/src/tool/get_paths.py")
    # print(yy)
    tt = p.join_path("parameters.yml")
    print(tt)