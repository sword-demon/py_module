import socket
import optparse
import json


class FtpClient(object):
    """ftp client"""

    # 消息最长1024
    MSG_SIZE = 1024

    def __init__(self):
        parser = optparse.OptionParser()
        parser.add_option("-s", "--server", dest="server", help="ftp server ip_addr")
        parser.add_option("-p", "--port", type="int", dest="port", help="ftp server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-p", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()

        print(self.options, self.args)

    def argv_verification(self):
        """检查参数合法性"""
        if not self.options.get('server') or not self.options.get("port"):
            # 任何一个少都不行
            exit("Error: must supply server and port parameters")

    def make_connection(self):
        """建立socket连接"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.options.server, self.options.port))

    def get_response(self):
        """获取服务器端返回内容"""
        data = self.sock.recv(self.MSG_SIZE)
        return json.loads(data.decode("utf-8"))

    def auth(self):
        """用户认证"""
        count = 0
        while count < 3:
            username = input("username: ").strip()
            if not username: continue
            password = input("password: ").strip()

            # 定义发送指令的规范
            cmd = {
                "action_type": "auth",
                "username": username,
                "password": password
            }
            self.sock.send(json.dumps(cmd).encode("utf-8"))
            response = self.get_response()
            print(response)
            if response.get("status_code") == 200:
                return True
            else:
                print(response.get("status_msg"))
            count += 1

    def intervactive(self):
        """处理与ftp server的交互"""
        if self.auth():
            pass


if __name__ == '__main__':
    client = FtpClient()
    # 交互
    client.intervactive()
