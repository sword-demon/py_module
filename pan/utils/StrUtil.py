import hashlib
from config import SALT


class StrUtil:
    """字符串工具类"""

    @staticmethod
    def md5(origin, salt=SALT):
        """md5加密"""
        hash_obj = hashlib.md5(salt.encode("utf-8"))
        hash_obj.update(origin.encode("utf-8"))
        return hash_obj.hexdigest()
