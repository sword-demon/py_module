import asyncio


async def func():
    print("hello world")


result = func()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(result)
asyncio.run(result)  # python3.7有的 更简单了
