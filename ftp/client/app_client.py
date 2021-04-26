import socket
import optparse
import json


class FtpClient(object):
    """ftp client"""

    # 消息最长1024
    MSG_SIZE = 1024

    def __init__(self):
        self.username = None
        parser = optparse.OptionParser()
        parser.add_option("-s", "--server", dest="server", help="ftp server ip_addr")
        parser.add_option("-P", "--port", type="int", dest="port", help="ftp server port")
        parser.add_option("-u", "--username", dest="username", help="username info")
        parser.add_option("-p", "--password", dest="password", help="password info")
        self.options, self.args = parser.parse_args()

        print(self.options, self.args)
        self.make_connection()

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
                self.username = username
                return True
            else:
                print(response.get("status_msg"))
            count += 1

    def intervactive(self):
        """处理与ftp server的交互"""
        if self.auth():
            while True:
                user_input = input("[%s]>>>:" % self.username).strip()
                if not user_input: continue

                cmd_list = user_input.strip()
                if hasattr(self, "_%s" % cmd_list[0]):
                    func = getattr(self, "_%s" % cmd_list[0])
                    func(cmd_list[1:])

    def parameter_check(self, args, min_args=None, max_args=None, exact_args=None):
        """参数个数合法性校验"""
        if min_args:
            if len(args) < min_args:
                print("must provide at least %s parameters, but %s received!" % (min_args, len(args)))
                return False
        if max_args:
            if len(args) > max_args:
                print("need at most %s parameters, but %s received!" % (max_args, len(args)))
                return False
        if exact_args:
            if len(args) != exact_args:
                print("need exactly %s parameters, but %s received!" % (max_args, len(args)))
                return False

        return True

    def send_msg(self, action_type, **kwargs):
        msg_data = {
            "action_type": action_type,
            "fill": ""
        }
        # 将两个字典合并到一起
        msg_data.update(kwargs)

        bytes_msgs = json.dumps(msg_data).encode("utf-8")
        if self.MSG_SIZE > len(bytes_msgs):
            msg_data["fill"] = msg_data["fill"].zfill(self.MSG_SIZE - len(bytes_msgs))
            bytes_msgs = json.dumps(msg_data).encode("utf-8")
        self.sock.send(bytes_msgs)

    def _get(self, cmd_args):
        """download files from ftp server
            1. 拿到文件名
            2. 发送到远程
            3. 等待服务器返回消息
                3.1 如果文件存在 拿到文件大小
                    3.1.1 循环接收
                3.2 文件如果不存在
                    print status_msg
        """
        if self.parameter_check(cmd_args, min_args=1):
            filename = cmd_args[0]
            self.send_msg(action_type="get", filename=filename)
            response = self.get_response()
            if response.get("status_code") == 301:
                # file exist ready to receive
                file_size = response.get("file_size")

                received_size = 0
                f = open(filename, mode="wb")
                while received_size < file_size:
                    if file_size - received_size < 8192:
                        data = self.sock.recv(file_size - received_size)
                    else:
                        data = self.sock.recv(8192)
                    received_size += len(data)
                    f.write(data)
                    print(received_size, file_size)
                else:
                    print("file [%s] recv done,file size [%s] " % (filename, file_size))
                    f.close()
            else:
                # status_code:300 file not exist
                print(response.get("status_msg"))

    def _put(self):
        pass


if __name__ == '__main__':
    client = FtpClient()
    # 交互
    client.intervactive()
