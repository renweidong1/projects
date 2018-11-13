from socket import *
import signal
import sys
import pymysql
import re
import os
import time

def main():
    db = pymysql.connect('localhost', 'root', '123456', 'dict')
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',8888))
    s.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
            print('connect from {}'.format(addr))
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue 
        pid = os.fork()
        if pid == 0:
            s.close()
            p = Child(c, db)
            p.menu()
        else:
            c.close()
class Child(object):
    def __init__(self, c, db):
        self.c = c
        self.db = db
    def menu(self):
        while True:
            msg = self.c.recv(128).decode()
            if not msg or msg[0] == 'E':
                self.c.close()
                sys.exit()#不能写成return
                # return
            else:
                m, self.n, self.p = re.split(r'[ ]', msg)
                if m == 'R':
                    self.do_register()
                elif m == 'L':
                    d = self.do_login()
                    if d == 1:
                        self.c.send(b'OK')
                    else:
                        self.c.send('用户名或者密码不正确'.encode())
                elif m == 'Q':
                    self.do_query()
    def do_register(self):
        cursor = self.db.cursor()
        sql = "select * from user where name='%s'" % self.n
        cursor.execute(sql)
        r = cursor.fetchone()
        if r == None:
            try:
                sql = "insert into user(name, password) values('%s','%s');"%(self.n, self.p)
                cursor.execute(sql)
            except Exception as e:
                print(e)
                self.db.rollback()
            else:
                self.db.commit()
                cursor.close()
                self.c.send(b'OK')
        else:
            self.c.send('用户名已存在'.encode())

    def do_login(self):
        cursor = self.db.cursor()
        sql = "select * from user where name='%s' and password='%s';" % (self.n,self.p)
        try:
            data = cursor.execute(sql)
        except Exception as e:
            return 0
            self.db.rollback()
        if cursor.fetchone() != None:
            return 1
        else:
            return 0

    def do_query(self):
        cursor = self.db.cursor()
        ur = self.p[0]+ 'zzzz'
        def insert_history():
            sql = "insert into history(time, name, word, inteper) values('%s','%s','%s','%s')" % \
            (time.ctime(), j, k, request[2])
            try:
                cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                return
        sql = "select * from words where word='%s' and word<= '%s'" % (self.p ,ur)
        try:
            cursor.execute(sql)
            request = cursor.fetchone()
            if request != None:
                self.c.send(b'OK')
                time.sleep(0.1)
                request1 = request[1] + ' ' + request[2]
                self.c.send(request1.encode())
                j = self.n
                k = self.p
                insert_history()#嵌套函数调用之前定义
            else:
                self.c.send('未找到'.encode())
        except Exception as e:
            self.c.send('查询异常'.encode())
            self.db.rollback()
            print(e)
            return








if __name__ == '__main__':
    main()


#sql语句返回的是查询结果个数，fetchone()可以获取查询结果


#嵌套函数调用之前定义
#def n():
#     m()
#     def m():
#         print(1)
# n()