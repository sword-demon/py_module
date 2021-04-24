import socket

from conf import settings


class FtpServer(object):
    """处于与客户端所有的交互的socket server"""

    def __init__(self, management_instance):
        self.management_instance = management_instance
        # 绑定socket实例对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((settings.HOST, settings.PORT))
        self.sock.listen(settings.MAX_SOCKET_LISTEN)

    def run_forever(self):
        """启动socket server"""
        print("starting ftp server on {}:{}".format(settings.HOST, settings.PORT).center(50, "-"))

        self.request, self.addr = self.sock.accept()
        print("got a new connection from {}".format(self.addr))
        self.handle()

    def handle(self):
        """处理所有的与用户的指令交互"""
        data = self.request.recv(1024)
        print("收到的data: ", data)
