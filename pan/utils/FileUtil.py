import shutil
import os
import sys

sys.path.append("/Users/wangxin/Desktop/python_learn/模块三 面向对象网络并发编程/pan")


class FileUtil:
    """文件工具类"""

    @staticmethod
    def show_all_dirs(path):
        """ls列出所有的目录"""
        file_list = os.listdir(path)
        return file_list

    @staticmethod
    def check_file_exists(file_path):
        if not os.path.exists(file_path):
            return False
        return True

    @staticmethod
    def rename_file(src, dest):
        """
        将原文件、文件夹重命名,移动原文件，文件夹到一个新的文件，文件夹
        :param src: 原文件，文件夹地址
        :param dest: 目标文件，文件夹地址
        :return: True/False
        """
        if not FileUtil.check_file_exists(dest) and os.path.isdir(dest):
            # 如果文件不存在且文件地址是一个目录，则新建一个目录
            os.mkdir(dest)
        try:
            shutil.move(src, dest)
        except Exception as e:
            print(str(e))
            return False

        return True
