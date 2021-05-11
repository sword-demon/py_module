from core import main


class ManagementTool(object):
    """负责对用户输入的指令进行解析并调用相应模块处理"""

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        print(self.sys_argv)
        self.verify_argv()

    def verify_argv(self):
        """验证指令合法性"""
        if len(self.sys_argv) < 2:
            self.help_msg()
        cmd = self.sys_argv[1]
        if not hasattr(self, cmd):
            print("invalid argument!")
            self.help_msg()

    @staticmethod
    def help_msg():
        msg = '''
        start       start FTP server
        stop        stop FTP　server
        restart     restart FTP server
        createuser  username    create a ftp user

        '''
        exit(msg)

    def execute(self, pool):
        """解析并执行指令"""
        cmd = self.sys_argv[1]
        func = getattr(self, cmd)
        func(pool)

    def start(self):
        """start ftp server"""
        # 这个地方有待优化，可以采用武sir的socketserver的方式
        server = main.FTPServer(self)
        server.run_forever()

    def create_user(self):
        print(self.sys_argv)
