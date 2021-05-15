import hashlib


def md5(file_name):
    m = hashlib.md5()
    m.update(file_name.encode("utf-8"))
    md5value = m.hexdigest()
    return md5value
