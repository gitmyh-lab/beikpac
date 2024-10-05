# mysql工具类的使用
import pymysql
from mysqlUtils import MysqlDB

# 实例化对象
my_db=MysqlDB()


# # 3.添加
# sql="insert into beke_data(name,age,address)values('tom',22,'wuhan')"
#
# # 4.调用方法
# my_db.commit_data(sql)

sql="select * from beke_data"
# 5.查询
print(my_db.select_one(sql))
