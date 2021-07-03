import asyncio
import aiohttp


async def fetch(session, url):
    print("发送请求", url)
    async with session.get(url, verify_ssl=False) as response:
        content = await response.content.read()
        file_name = url.rsplit("_")[-1]
        with open(file_name, mode="wb") as f:
            f.write(content)
        print("下载完成", url)


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQG0Hl2WQnmhO_Sp_BAyjjA4y4LJLwu5M9POA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvESXKroHI5muX_tRMN8UFOLVP1KRXmLzE-Q&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGI_d5Jb-PsXf5lPHB0P9BGxsWd8q3tCUOow&usqp=CAU"
        ]
        tasks = [asyncio.create_task(fetch(session, url)) for url in url_list]

        await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())
