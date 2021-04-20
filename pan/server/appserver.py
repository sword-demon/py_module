import socket
from openpyxl import load_workbook
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8001))
sock.listen(10)

while True:
    conn, addr = sock.accept()

    client_data = conn.recv(1024).decode("utf-8")  # 等待客户端发来数据
    # 解析客户端传递的请求信息

    """
    这里可以设计为使用反射将字符串进行反射到类方法里去，进行运行对应的功能
    """
