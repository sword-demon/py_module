from urllib.parse import parse_qs

import pymysql


def login(environ):
    with open("templates/login.html", mode="rb") as f:
        data = f.read()
    return data


def index(environ):
    with open("templates/index.html", mode="rb") as f:
        data = f.read()
    return data


def auth(request):
    """登录验证"""
    try:
        # 获取请求的大小
        request_body_size = int(request.get("CONTENT_LENGTH", 0))
    except ValueError:
        request_body_size = 0

    request_body = request['wsgi.input'].read(request_body_size)
    data = parse_qs(request_body)

    user = data.get(b"user")[0].decode("utf8")
    pwd = data.get(b"pwd")[0].decode("utf8")

    # 连接数据库
    conn = pymysql.connect(host="127.0.0.1", port=3306,
                           user="root", password="", db="web")  # 前提你得有一个数据库叫web

    # 创建游标
    cursor = conn.cursor()

    sql = "select * from user_info where name= '%s' and password = '%s'" % (user, pwd)
    cursor.execute(sql)

    if cursor.fetchone():
        # 成功返回首页
        return index(request)
    else:
        return b"user or pwd is wrong"
