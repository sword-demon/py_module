from wsgiref.simple_server import make_server


def application(environ, start_response):
    # 按着http请求协议解析数据: environ
    # 按着http响应协议进行组装数据: start_response

    # 响应首行 响应头
    start_response('200 OK', [("Content-Type", "text/html")])

    print(environ, type(environ))

    # 当前的请求路径
    path = environ.get("PATH_INFO")
    if path == "/login":
        return ["login".encode("utf8")]
    elif path == "/index":
        return ["index".encode("utf8")]

    return [b"<h1>hello web</h1>"]


# socket已经被封装了, 后面无需我们自己手写
httped = make_server("", 8090, application)

# 等待用户连接 => conn, addr = socket.accept()
httped.serve_forever()
