import os

# 基础目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HOST = "127.0.0.1"  # 服务端IP 用于服务端进行绑定使用
PORT = 8080  # 服务端 端口

# 是否允许IP端口重用
ALLOW_REUSE_ADDRESS = True

# 设置最大传输数据量
MAX_PACKET_SIZE = 8192

# 设置socket监听个数
MAX_SOCKET_LISTEN = 5

# 用户家目录
USER_HOME_DIR = os.path.join(BASE_DIR, 'home')

# 用户信息存储文件
ACCOUNT_FILE = os.path.join(BASE_DIR, 'conf', 'accounts.ini')

# 最大的并发数量
MAX_THREAD_NUM = 10
