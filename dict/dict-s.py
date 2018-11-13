from socket import *
import sys
import os
import pymysql
import time

class DictServer(object):
    #创建套接字，数据库对象
    def __init__(self, addr):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.s.bind(addr)
        self.s.listen(5)

        self.db = pymysql.connect("localhost","root","123456","dict",charset="utf8")
        self.cursor = self.db.cursor()
    #用户登录处理
    def do_login(self, c, info):
        sel = "select name from user where name=%s and password=%s"
        try:
            num = self.cursor.execute(sel,info)
        except Exception as e:
            print(e)
        else:
            if not num:
                c.send("用户名或者密码错误".encode())
            else:
                c.send(b'OK')

    #用户注册
    def do_register(self, c, name, password):
        sel = "select name from user where name=%s"
        try:
            num = self.cursor.execute(sel,[name])
        except Exception as e:
            print(e)
        else:
            if num:
                c.send("用户已经存在".encode())
            else:
                ins = "insert into user(name, password) values(%s,%s)"
                try:
                    self.cursor.execute(ins,[name,password])
                    self.db.commit()
                    c.send(b'OK')
                except Exception as e:
                    print(e)
                    c.send('注册出现异常'.encode())
                    self.db.rollback()

    # 查词
    def querywords(self, c, name, word):
        sel = "select id,word,interpreter from words where word=%s"
        def inserthistory(name):
            sel = "select id from user where name=%s"
            try:
                self.cursor.execute(sel,[name])
            except Exception as e:
                print(e)
            else:
                name_id = self.cursor.fetchone()[0]
                word_id = result[0]
                t = time.ctime()
                ins = "insert into history(name_id,word_id) values(%s,%s)"
                try:
                    self.cursor.execute(ins,[name_id,word_id])
                    self.db.commit()
                except Exception as e:
                    print(e)
                    self.db.rollback()
        try:
            self.cursor.execute(sel,[word])
            result = self.cursor.fetchone()
        except Exception as e:
            print(e)
        else:
            if result:
                c.send("#".join(result[1:]).encode())
                inserthistory(name)#添加历史记录
            else:
                c.send("no".encode())




    def queryhistory(self, c, name):
        sel = "select id from user where name=%s"
        self.cursor.execute(sel,[name])
        name_id = self.cursor.fetchone()[0]
        sel1 = "select word,interpreter from words where id in (select word_id from history where name_id=%s)"
        self.cursor.execute(sel1,[name_id])
        words = self.cursor.fetchall()
        if words:
            result = ''
            for tup in words:
                result =result + "   ".join(tup) + "\n"
            c.send(result.encode())
            time.sleep(0.5)
            c.send("##".encode())
        else:
            c.send('none'.encode())

    #子进程
    def do_child(self, c):
        while True:
            try:
                data = c.recv(1024).decode().strip().split(" ")
            except Exception as e:
                print(e)
            else:
                # 客户端断开连接
                if not data or data[0] == 'Q':
                    c.close()
                    sys.exit("客户端退出")
                if data[0] == "L":
                    info = [data[1], data[2]]
                    self.do_login(c, info)
                elif data[0] == "R":
                    name, password = data[1], data[2]
                    self.do_register(c, name, password)
                elif data[0] == "C":
                    name, word = data[1], data[2]
                    self.querywords(c, name, word)
                elif data[0] == "H":
                    name = data[1]
                    self.queryhistory(c, name)

    #通信和并发
    def main(self):
        while True:
            try:
                c, addr = self.s.accept()
                print(addr)
                pid = os.fork()
                if pid == 0:
                    self.do_child(c)
                    self.s.close()#关闭子进程中多余套接字
                else:
                    c.close()
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8889
    addr = (host,port)
    DictServer(addr).main()
