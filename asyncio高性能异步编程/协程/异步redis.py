import aioredis
import asyncio


async def execute(address, password):
    print("开始执行", address)
    # 网络IO操作，创建redis链接
    redis = await aioredis.create_redis(address, password=password)

    # 网络IO操作，在redis里设置哈希值car，内部设置3个键值对
    await redis.hmset_dict("car", key1=1, key2=2, key3=3)

    # 网络IO操作，去redis中获取值
    result = await redis.hgetall("car", encoding="utf-8")
    print(result)

    redis.close()
    # 网络IO操作，关闭redis
    await redis.wait_closed()

    print("结束", address)


asyncio.run(execute("redis://127.0.0.1:6379", ""))
