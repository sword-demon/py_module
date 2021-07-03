import requests


def download_images(url):
    print("开始下载:", url)
    # 发送网络请求，下载图片
    response = requests.get(url)
    print("下载完成")
    # 图片保存到本地
    file_name = url.rsplit("_")[-1]
    with open(file_name, mode="wb") as f:
        f.write(response.content)


if __name__ == '__main__':
    url_list = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG0Hl2WQnmhO_Sp_BAyjjA4y4LJLwu5M9POA&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvESXKroHI5muX_tRMN8UFOLVP1KRXmLzE-Q&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGI_d5Jb-PsXf5lPHB0P9BGxsWd8q3tCUOow&usqp=CAU"
    ]

    for item in url_list:
        download_images(item)
