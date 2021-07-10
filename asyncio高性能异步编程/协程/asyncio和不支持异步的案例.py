import asyncio
import requests


async def download_image(url):
    # 发生网络请求，下载图片，(遇到网络下载的IO请求，自动切换到其他任务)
    print("开始下载：", url)

    loop = asyncio.get_event_loop()

    # requests模块不支持异步操作，所以就使用线程池来配合实现
    future = loop.run_in_executor(None, requests.get, url)

    response = await future
    print("下载完成")
    # 图片保存到本地
    file_name = url.rsplit('_')[-1]
    with open(file_name, mode="wb") as file_object:
        file_object.write(response.content)


if __name__ == '__main__':
    url_list = [
        '图片.jpg'
    ]

    tasks = [download_image(url) for url in url_list]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
