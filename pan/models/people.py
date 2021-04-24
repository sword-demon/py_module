from utils.StrUtil import StrUtil


class User:
    """用户类"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        if self.username == "alex" and StrUtil.md5(self.password) == "dwqdwqdwqqwdqwdqwdq":
            print("登陆成功")
