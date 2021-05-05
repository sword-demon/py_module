import os
import socket
import optparse
import json


class FtpClient(object):
    """ftp client"""

    # 消息最长1024
    MSG_SIZE = 1024

    def __init__(self):
        self.username = None
        # 用户交互显示
        self.terminal_display = None
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
                self.terminal_display = "[%s]>>>:" % self.username
                return True
            else:
                print(response.get("status_msg"))
            count += 1

    def intervactive(self):
        """处理与ftp server的交互"""
        if self.auth():
            while True:
                user_input = input(self.terminal_display).strip()
                if not user_input: continue

                cmd_list = user_input.strip()
                print(cmd_list[0])
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

    def _ls(self, cmd_args):
        """display current dir's file list"""
        self.send_msg(action_type="ls")
        response = self.get_response()  # 1024
        print(response)
        if response.get("status_code") == 302:
            # ready to send long msg
            cmd_result_size = response.get("cmd_result_size")
            received_size = 0
            cmd_result = b""
            while received_size < cmd_result_size:
                if cmd_result_size - received_size < 8192:
                    data = self.sock.recv(cmd_result_size - received_size)
                else:
                    data = self.sock.recv(8192)
                cmd_result += data
                received_size += len(data)
            else:
                print(cmd_result.decode("gbk"))

    def _cd(self, cmd_args):
        """change to target dir 切换目录"""
        # 必须有一个参数
        if self.parameter_check(cmd_args, exact_args=1):
            target_dir = cmd_args[0]
            self.send_msg(action_type="cd", target_dir=target_dir)
            response = self.get_response()
            print(response)
            if response.get("status_code") == 350:
                # dir changed successfully
                self.terminal_display = "[/%s]" % response.get("current_dir")

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
        print(cmd_args)
        if self.parameter_check(cmd_args, min_args=1):
            filename = cmd_args[0]
            self.send_msg(action_type="get", filename=filename)
            response = self.get_response()
            if response.get("status_code") == 301:
                # file exist ready to receive
                file_size = response.get("file_size")

                received_size = 0
                progress_generator = self.progress_bar(file_size)
                progress_generator.__next__()
                f = open(filename, mode="wb")
                while received_size < file_size:
                    if file_size - received_size < 8192:
                        data = self.sock.recv(file_size - received_size)
                    else:
                        data = self.sock.recv(8192)
                    received_size += len(data)
                    f.write(data)
                    progress_generator.send(received_size)
                    # print(received_size, file_size)
                else:
                    print("file [%s] recv done,file size [%s] " % (filename, file_size))
                    f.close()
            else:
                # status_code:300 file not exist
                print(response.get("status_msg"))

    def progress_bar(self, total_size):
        current_percent = 0
        last_percent = 0
        while True:
            received_size = yield current_percent
            current_percent = int(received_size / total_size * 100)
            if current_percent > last_percent:
                print("#" * int(current_percent / 2) + "{}%".format(current_percent), end="\r", flush=True)
                # 把本次循环的百分比赋值给上一次的
                last_percent = current_percent

    def _put(self, cmd_args):
        """上传本地文件到服务器
        1. 确保本地文件存在
        2. 拿到文件名+大小，放到消息头里发送给服务端
        3. 打开文件，发送内容
        """
        if self.parameter_check(cmd_args, exact_args=1):
            local_file = cmd_args[0]
            if os.path.isfile(local_file):
                total_size = os.path.getsize(local_file)
                self.send_msg(action_type="put", file_size=os.path.getsize(local_file), filename=local_file)
                f = open(local_file, mode="rb")
                uploaded_size = 0

                progress_generator = self.progress_bar(total_size)
                progress_generator.__next__()
                for line in f:
                    self.sock.send(line)
                    uploaded_size += len(line)
                    progress_generator.send(uploaded_size)

                    # current_percent = int(uploaded_size / total_size * 100)
                    # if current_percent > last_percent:
                    #     print("#" * int(current_percent / 2) + "{}%".format(current_percent), end="\r", flush=True)
                    #     # 把本次循环的百分比赋值给上一次的
                    #     last_percent = current_percent
                else:
                    print("file upload done".center(50, "-"))
                    f.close()


if __name__ == '__main__':
    client = FtpClient()
    # 交互
    client.intervactive()
