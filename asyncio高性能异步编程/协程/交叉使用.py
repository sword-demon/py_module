import time
import asyncio
import concurrent.futures


def func1():
    # 某个耗时操作
    time.sleep(2)
    return "SB"


async def main():
    loop = asyncio.get_running_loop()

    # 将不支持协程的进行转换
    fut = loop.run_in_executor(None, func1)
    result = await fut
    print("default thread pool", result)


asyncio.run(main())
