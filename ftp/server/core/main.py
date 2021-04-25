import configparser
import hashlib
import json
import socket

from conf import settings


class FtpServer(object):
    """处于与客户端所有的交互的socket server"""

    STATUS_CODE = {
        200: "Passed authentication",
        201: "wrong username or password",
        300: "file does not exist!"
    }

    # 消息最长1024
    MSG_SIZE = 1024

    def __init__(self, management_instance):
        self.management_instance = management_instance
        # 绑定socket实例对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((settings.HOST, settings.PORT))
        self.sock.listen(settings.MAX_SOCKET_LISTEN)
        self.accounts = self.load_accounts()

    def run_forever(self):
        """启动socket server"""
        print("starting ftp server on {}:{}".format(settings.HOST, settings.PORT).center(50, "-"))

        while True:
            self.request, self.addr = self.sock.accept()
            print("got a new connection from {}".format(self.addr))
            self.handle()

    def handle(self):
        """处理所有的与用户的指令交互"""
        while True:
            raw_data = self.request.recv(1024)
            print("收到的data: ", raw_data)
            if not raw_data:
                print("connection %s is lost" % (self.addr,))
                del self.request, self.addr
                break
            data = json.loads(raw_data).decode("utf-8")
            action_type = data.get("action_type")
            if action_type:
                if hasattr(self, "_%s" % action_type):
                    func = getattr(self, "_%s" % action_type)
                    func(data)
            else:
                print("Invalid command!")

    def load_accounts(self):
        """加载所有账号信息"""
        config_obj = configparser.ConfigParser()
        config_obj.read(settings.ACCOUNT_FILE)

        # print(config_obj.sections())
        return config_obj

    def authenticate(self, username, password):
        """用户认证方法"""
        if username in self.accounts:
            _password = self.accounts[username]['password']
            md5_obj = hashlib.md5()
            md5_obj.update(password.encode("utf-8"))
            if _password == md5_obj.hexdigest():
                print("passed authentication...")
                return True
            else:
                print("wrong username or password")
                return False
        else:
            print("wrong username or password")
            return False

    def send_response(self, status_code, *args, **kwargs):
        """
        打包发送消息给客户端
        :param status_code:
        :param args:
        :param kwargs:
        :return:
        """
        data = kwargs
        data["status_code"] = status_code
        data["status_msg"] = self.STATUS_CODE[status_code]
        data["fill"] = ""

        bytes_data = json.dumps(data).encode("utf-8")
        if len(bytes_data) < self.MSG_SIZE:
            data["fill"] = data["fill"].zfill(self.MSG_SIZE - len(bytes_data))
            bytes_data = json.dumps(data).encode("utf-8")

        self.request.send(bytes_data)

    def _auth(self, data):
        """处理用户认证请求"""
        print("auth ", data)
        if self.authenticate(data.get("username"), data.get("password")):
            print("passed auth")

            # 返回消息
            # 1. 消息内容 状态码
            # 2. json.dumps
            # 3. encode
            self.send_response(stats_code=200)
        else:
            self.send_response(stats_code=201)
