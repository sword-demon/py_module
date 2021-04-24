import os

# server 基础地质
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "0.0.0.0"
PORT = 9999

# 家目录
USER_HOME_DIR = os.path.join(BASE_DIR, "home")

# 存储用户账号的配置
ACCOUNT_FILE = "%s/conf/accounts.ini" % BASE_DIR

# 最大监听数量
MAX_SOCKET_LISTEN = 5
