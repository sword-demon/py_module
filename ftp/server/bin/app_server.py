# 添加环境变量
import os
import sys

# 让他可以调用server目录下面的其他包里的模块
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)

# 将server 添加进入环境变量
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from core import management

    argv_parser = management.ManagementTool(sys.argv)
    argv_parser.execute()
