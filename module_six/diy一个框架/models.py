# 在数据库中生成用户表
import pymysql


# 连接数据库
conn = pymysql.connect(host="127.0.0.1", port=3306,
                       user="root", password="", db="web")  # 前提你得有一个数据库叫web

# 创建游标
cursor = conn.cursor()

# 编写sql语句
sql = """
create table user_info (
    id INT PRIMARY KEY,
    name varchar(50),
    password varchar(32)
)
"""

# 执行sql语句
cursor.execute(sql)

# 提交
conn.commit()
# 关闭游标
cursor.close()

# 关闭连接
conn.close()
