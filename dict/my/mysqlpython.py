from pymysql import *

class mysqlpython:
    def __init__(self,host,port,db,user,passwd,
                 charset="utf8"):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

    def open(self):
        self.conn = connect(host=self.host,port=
               self.port,db=self.db,user=self.user,
               passwd=self.passwd,
               charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def zhixing(self,sql):
        self.open()
        self.cursor.execute(sql)
        self.conn.commit()
        self.close()
        print("ok")

from mysqlpython import mysqlpython

# 创建实例化对象
sqlh = mysqlpython("localhost",3306,"db2","root",
                   "123456")

sql_update = "update sheng set id=150 where id=1;"
sqlh.zhixing(sql_update)


# --------------------------------------------------------------




import pymysql

db = pymysql.connect("localhost","root","123456",
                     "db2",charset="utf8")
cur = db.cursor()

sql_select = "select * from city;"
cur.execute(sql_select)

data = cur.fetchone()
print("fetchone的结果为",data)

data2 = cur.fetchmany(2)
print("fetchmany(2)的结果如下:")
for i in data2:
    print(i)

data3 = cur.fetchall()
print("fetchall()的结果如下：")
for i in data3:
    print(i)

db.commit()
cur.close()
db.close()


# --------------------------------------------------------------

import pymysql

db = pymysql.connect("localhost","root","123456",
                     "db2",charset="utf8")
cur = db.cursor()

try:
    cur.execute("update CCB set money=5000 where \
                 name='Zhuanqian';")
    cur.execute("update ICBC set money=9000 where \
                 name='Shouqian';")
    db.commit()
    print("ok")
except Exception as e:
    db.rollback()
    print("出现错误，已回滚")

cur.close()
db.close()

# --------------------------------------------------------------

























