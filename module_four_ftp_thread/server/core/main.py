import socket
from conf import settings
import json, hashlib, os, time
import configparser
import subprocess
import platform


class UtilBase:
    LOG_DIR = settings.LOG_DIR

    def logger(self, level='error', content=''):
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file_name = "{}.log".format(time_now)
        file_path = os.path.join(self.LOG_DIR, file_name)
        format_content = "{}.{},{}\n".format(time_str, level, content)
        with open(file_path, mode="a", encoding="utf-8") as f:
            f.write(format_content)

    def md5(self, file_name):
        m = hashlib.md5()
        m.update(file_name.encode("utf-8"))
        md5value = m.hexdigest()
        return md5value


class FTPServer(object):
    """处理与客户端所有的交互的socket server"""

    STATUS_CODE = {
        200: "Passed authentication!",
        201: "Wrong username or password!",
        300: "File does not exist !",
        301: "File exist , and this msg include the file size- !",
        302: "This msg include the msg size!",
        350: "Dir changed !",
        351: "Dir doesn't exist !",
        401: "File exist ,ready to re-send !",
        402: "File exist ,but file size doesn't match!",
    }

    MSG_SIZE = settings.MAX_PACKET_SIZE  # 消息最长1024
    # 是否可以iP,端口复用
    allow_reuse_address = settings.ALLOW_REUSE_ADDRESS

    def __init__(self, management_instance, bind_and_active=True):
        self.management_instance = management_instance
        # 实例化套接字对象
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 初始化加载用户数据
        self.accounts = self.load_accounts()
        self.user_obj = None
        self.user_current_dir = None

        if bind_and_active:
            try:
                self.server_bind()
                self.server_active()
            except Exception as e:
                print(str(e))
                print("连接断开")
                self.server_close()

    def run_forever(self, pool):
        """启动socket server"""
        print('starting FTP server on %s:%s'.center(50, '-') % (settings.HOST, settings.PORT))

        while True:
            request, addr = self.get_request()
            print("got a new connection from %s....." % (addr,))
            if not pool.is_empty():
                print("当前暂无可用的线程")
            t = pool.get_thread()
            obj = t(target=MyHandler, args=(request, addr))
            obj.start()

    def server_close(self):
        """关闭服务端"""
        self.sock.close()

    def server_bind(self):
        """绑定IP端口，是否IP端口复用"""
        if self.allow_reuse_address:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((settings.HOST, settings.PORT))

    def server_active(self):
        """监听客户端连接数"""
        self.sock.listen(settings.MAX_SOCKET_LISTEN)

    def get_request(self):
        """接收客户端连接"""
        return self.sock.accept()

    def close_request(self, request):
        """关闭单个连接"""
        request.close()

    def load_accounts(self):
        """加载所有账号信息"""
        config_obj = configparser.ConfigParser()
        config_obj.read(settings.ACCOUNT_FILE)

        # print(config_obj.sections())
        return config_obj


class MyHandler(FTPServer, UtilBase):

    def __init__(self, request, addr):
        super().__init__(request, addr)
        self.request = request
        self.addr = addr
        try:
            self.handle()
        except Exception as e:
            print("Error happened with client,close connection.", e)
            self.request.close()

    def handle(self):
        """处理与用户的所有指令交互"""
        while True:
            raw_data = self.request.recv(self.MSG_SIZE)
            print('------->', raw_data)
            if not raw_data:
                # 数据为空，断开连接
                print("connection %s is lost ...." % (self.addr,))
                del self.request, self.addr
                break

            data = json.loads(raw_data.decode("utf-8"))
            action_type = data.get('action_type')  # None
            if action_type:
                if hasattr(self, "_%s" % action_type):
                    func = getattr(self, "_%s" % action_type)
                    func(data)

            else:
                print("无此功能...")

    def authenticate(self, username, password):
        """用户认证方法"""
        if username in self.accounts:
            _password = self.accounts[username]['password']
            md5_obj = hashlib.md5()
            md5_obj.update(password.encode())
            md5_password = md5_obj.hexdigest()
            print("passwd:", _password, md5_password)
            if md5_password == _password:
                # print("passed authentication...")
                # set user obj
                self.user_obj = self.accounts[username]
                # self.current_user_home= os.path.join(settings.USER_HOME_DIR,username)
                self.user_obj['home'] = os.path.join(settings.USER_HOME_DIR, username)  # /home/alex
                # set user home directory
                self.user_current_dir = self.user_obj['home']
                # self.logger('error', self.user_current_dir)
                # self.logger('error', str(not os.path.isdir(self.user_current_dir)))
                # self.logger('error', str(not os.path.exists(self.user_current_dir)))
                if not os.path.exists(self.user_current_dir):
                    # 设置了用户目录，还需要为用户新建目录
                    os.mkdir(self.user_current_dir)
                return True
            else:
                # print("wrong username or password ")
                return False
        else:
            # print("wrong username or password 2")
            return False

    def send_response(self, status_code, *args, **kwargs):
        """
        打包发送消息给客户端
        :param status_code:
        :param args:
        :param kwargs: {filename:ddd,filesize:222}
        :return:
        """
        data = kwargs
        data['status_code'] = status_code
        data['status_msg'] = self.STATUS_CODE[status_code]
        data['fill'] = ''

        bytes_data = json.dumps(data).encode()

        if len(bytes_data) < self.MSG_SIZE:
            data['fill'] = data['fill'].zfill(self.MSG_SIZE - len(bytes_data))
            bytes_data = json.dumps(data).encode()

        self.request.send(bytes_data)

    def _auth(self, data):
        """处理用户认证请求"""
        print("auth ", data)
        if self.authenticate(data.get('username'), data.get('password')):
            print('pass auth....')

            # 1. 消息内容，状态码
            # 2. json.dumps
            # 3 . encode
            self.send_response(status_code=200)

        else:
            self.send_response(status_code=201)

    def _get(self, data):
        """client downloads file through this method
            1. 拿到文件名
            2. 判断文件是否存在
                2.1 如果存在， 返回状态码+文件大小
                    2.1.1打开文件，发送文件内容
                2.2 如果不存在， 返回状态码
            3.
        """
        filename = data.get('filename')
        # full_path = os.path.join(self.user_obj['home'],filename)
        full_path = os.path.join(self.user_current_dir, filename)
        if os.path.isfile(full_path):
            filesize = os.stat(full_path).st_size
            self.send_response(301, file_size=filesize)
            print("ready to send file ")
            f = open(full_path, 'rb')
            for line in f:
                self.request.send(line)
            else:
                print('file send done..', full_path)
            f.close()
        else:
            self.send_response(300)

    def _re_get(self, data):
        """re-send file to client
        1. 拼接文件路径
        2. 判断文件是否存在
            2.1 如果存在，判断文件大小是否与客户端发过来的一致
                2.1.1 如果不一致，返回错误消息
                2.1.2 如果一致，告诉客户端，准备续传吧
                2.1.3 打开文件，Seek到指定位置，循环发送
            2.2 文件不存在，返回错误
        """
        # print("_re_get", data)
        abs_filename = data.get('abs_filename')
        # 这里反斜杠和正斜杠，系统之分，fuck!
        full_path = os.path.join(self.user_obj['home'], abs_filename.strip(os.sep))
        # print("reget fullpath", full_path)
        # print("user home", self.user_obj['home'])
        # self.logger('error', os.path.join(self.user_obj['home'], abs_filename.strip("\\")))
        if os.path.isfile(full_path):  # 2.1
            if os.path.getsize(full_path) == data.get('file_size'):  # 2.1.2
                self.send_response(401)
                f = open(full_path, 'rb')
                f.seek(data.get("received_size"))
                for line in f:
                    self.request.send(line)
                else:
                    print("-----file re-send done------")
                    f.close()
            else:  # 2.1.1
                self.send_response(402, file_size_on_server=os.path.getsize(full_path))
        else:
            self.send_response(300)

    def _put(self, data):
        """client uploads file to server
        1. 拿到local文件名+大小+md5值
        2. 检查本地是否已经有相应的文件。self.user_cuurent_dir/local_file
            2.1 if file exist , create a new file with file.timestamp suffix.
            2.2 if not , create a new file named local_file name
        3. start to receive data
        """
        local_file = data.get("filename")
        md5value = data.get("md5_value")
        self.logger('error', str(type(local_file)))
        self.logger('error', str(type(md5value)))
        self.logger('error', local_file)
        if self.md5(local_file) == md5value:
            full_path = os.path.join(self.user_current_dir, local_file)  # 文件
            if os.path.isfile(full_path):  # 代表文件已存在，不能覆盖，
                filename = "%s.%s" % (full_path, time.time())
            else:
                filename = full_path

            f = open(filename, "wb")
            total_size = data.get('file_size')
            received_size = 0

            while received_size < total_size:
                if total_size - received_size < 8192:  # last recv
                    data = self.request.recv(total_size - received_size)
                else:
                    data = self.request.recv(8192)
                received_size += len(data)
                f.write(data)
                print(received_size, total_size)
            else:
                print('file %s recv done' % local_file)
                f.close()
        else:
            print("file is not same from user upload")
            self.send_response(402)

    @staticmethod
    def __get_os_dir_list_command():
        """根据不同系统获取对应的展示目录的命令"""
        if platform.system() == 'Windows':
            command = "dir"
        elif platform.system() == 'Linux':
            command = "ls"
        else:
            command = "ls"
        return command

    def _ls(self, data):
        """run dir command and send result to client"""
        command = self.__get_os_dir_list_command()
        cmd_obj = subprocess.Popen('%s %s' % (command, self.user_current_dir), shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()

        cmd_result = stdout + stderr

        if not cmd_result:
            cmd_result = b'current dir has no file at all.'

        self.send_response(302, cmd_result_size=len(cmd_result))
        self.request.sendall(cmd_result)

    def _cd(self, data):
        """根据用户的target_dir改变self.user_current_dir 的值
        1. 把target_dir 跟user_current_dir 拼接
        2. 检测 要切换的目录是否存在
            2.1 如果存在 ， 改变self.user_current_dir的值到新路径
            2.2 如果不存在，返回错误消息

        """
        target_dir = data.get('target_dir')
        full_path = os.path.abspath(os.path.join(self.user_current_dir, target_dir))  # abspath是为了解决../..的问题
        print("full path:", full_path)
        if os.path.isdir(full_path):

            if full_path.startswith(self.user_obj['home']):  # has permission
                self.user_current_dir = full_path
                relative_current_dir = self.user_current_dir.replace(self.user_obj['home'], '')
                self.send_response(350, current_dir=relative_current_dir)

            else:
                self.send_response(351)

        else:
            self.send_response(351)
