from wsgiref.simple_server import make_server


def application(environ, start_response):
    # 按着http请求协议解析数据: environ
    # 按着http响应协议进行组装数据: start_response

    # 响应首行 响应头
    start_response('200 OK', [("Content-Type", "text/html")])

    print(environ.get("PATH_INFO"))

    # 当前的请求路径
    path = environ.get("PATH_INFO")
    print(path)

    # 方式1
    # if path == "/login":
    #     return ["login".encode("utf8")]
    # elif path == "/index":
    #     with open("index.html", mode="rb") as f:
    #         data = f.read()
    #     return [data]
    #
    # return [b"<h1>hello web</h1>"]

    # 方式2
    # 路径解耦， 路径对应一个函数
    # url_patterns = [
    #     ("/login", login),
    #     ("/index", index),
    # ]

    # 方式3将函数和url进行分离
    from urls import url_patterns

    func = None
    # 遍历列表
    for item in url_patterns:
        # 如果当前请求路径和元组的第一个元素匹配
        if path == item[0]:
            func = item[1]
            break
    # 判断是否都匹配成功
    if func:
        # 执行函数
        return [func(environ)]
    else:
        return [b"404"]


# socket已经被封装了, 后面无需我们自己手写
httped = make_server("", 8090, application)

# 等待用户连接 => conn, addr = socket.accept()
httped.serve_forever()
