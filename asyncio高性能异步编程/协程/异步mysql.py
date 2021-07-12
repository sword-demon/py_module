import asyncio
import aiomysql


async def execute():
    # 网络IO操作，连接mysql
    conn = await aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='mysql', )

    # 网络IO操作，创建游标
    cur = await conn.cursor()

    # 执行sql
    await cur.execute("select user,host from user")

    # 网络IO操作，获取SQL执行结果
    result = await cur.fetchall()
    print(result)

    # 网络IO操作，关闭连接
    await cur.close()
    conn.close()


asyncio.run(execute())
