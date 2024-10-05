"""

    封装mysql工具类，可以实现mysql的基本操作
    步骤：
        1.链接数据库
        2.获取对象,获取游标
        3.执行sql语句的操作
"""
import pymysql
# 配置参数
config={
    "host":"127.0.0.1",
    "port":3306,
    "charset":"utf8",
    "database":"bk_data",
    "user":"root",
    "password":"123456"
}

class MysqlDB():
    def __init__(self):
        self.conn=self.get_conn()
        # 调用游标
        self.cursor=self.get_cursor()
        pass
    # 创建数据库函数
    def get_conn(self):
        conn=pymysql.connect(**config)
        return conn
        pass
    # 获取游标
    def get_cursor(self):
        cursor=self.conn.cursor()
        return cursor
        pass
    # 查询
    def select_one(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()
        pass

    # 插入数据
    def commit_data(self,sql):
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交
            self.conn.commit()
            # 提示语句
            print("数据提交成功!")
            pass
        except Exception as e:
            print("提交数据失败",e)
            # 数据回滚
            self.conn.rollback()
            pass
        pass
















