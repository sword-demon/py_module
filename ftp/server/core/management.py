from core import main


class ManagementTool(object):
    """负责对用户输入的指令进行解析并调用相应的模块处理"""

    def __init__(self, sys_argv):
        # 默认是一个列表，且里面有一个元素，所以最小要有一个参数，长度不能小于2
        self.sys_argv = sys_argv
        self.verify_argv()

    def verify_argv(self):
        """验证指令是否合法"""
        if len(self.sys_argv) < 2:
            self.help_msg()
        cmd = self.sys_argv[1]
        # 判断当前类是否有这个方法
        if not hasattr(self, cmd):
            print("invalid argument!")
            self.help_msg()

    @staticmethod
    def help_msg():
        """msg
        start   start ftp server
        stop    stop ftp server
        restart restart ftp server
        createuser username create a ftp user
        """
        msg = '''
        start   start ftp server
        stop    stop ftp server
        restart restart ftp server
        createuser username create a ftp user
        '''
        exit(msg)

    def execute(self):
        """解析指令并执行"""
        cmd = self.sys_argv[1]
        func = getattr(self, cmd)
        func()

    def start(self):
        """start ftp server"""
        server = main.FtpServer(self)
        server.run_forever()
