import asyncio


class AsyncContextManager:

    def __init__(self):
        # self.conn = conn
        pass

    async def do_something(self):
        # 异步操作数据库
        return 666

    async def __aenter__(self):
        # 异步连接数据库
        # self.conn = await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 异步关闭数据库
        await asyncio.sleep(1)


async def func():
    obj = AsyncContextManager()
    async with obj:
        result = await obj.do_something()
        print(result)


asyncio.run(func())
