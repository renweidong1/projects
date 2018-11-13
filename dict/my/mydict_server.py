from socket import *
import signal
import sys
import os
import re
import pymysql
import time

def main():
    db = pymysql.connect('localhost', 'root','123456','dict')
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8888))
    s.listen(5)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
            print('connect from', addr)
        except KeyboardInterrupt:
            sys.exit('服务器异常')
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c, db)
        else:
            c.close()
            continue

def do_child(c, db):
    while True:
        d = c.recv(1024).decode().split(' ')
        if (not d) or d[0] == 'E':
            c.close()
            sys.exit(0)
        elif d[0] == 'H':
            do_history(c, db, d[1])
        else:
            if d[0] == 'R':
                data = do_register(c, db, d[1], d[2])
                if data == 0:
                    c.send('数据库出现异常'.encode())
            elif d[0] == 'L':
                do_login(c, db, d[1], d[2])
            elif d[0] == 'Q':
                do_query(c, db, d[1], d[2])

def do_register(c, db, name, password):
    name, password = name, password
    cursor = db.cursor()
    sql = "select * from user where name='%s'" % name
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
    except:
        db.rollback()
        return 0
    if data == None:
        sql = "insert into user(name, password) values('%s','%s')" % (name, password)
        try:
            cursor.execute(sql)
        except:
            db.rollback()
            return 0
        db.commit()
        cursor.close()
        c.send(b'OK')
    else:
        c.send('用户名已存在'.encode())

def do_login(c, db, name, password):
    cursor = db.cursor()
    sql = "select * from user where name='%s' and password='%s';" % (name, password)
    try:
        cursor.execute(sql)
        data = cursor.fetchone()
    except:
        db.rollback()
        c.send('false'.encode())
    if data:
        c.send(b'OK')
    else:
        c.send('登录失败'.encode())

def do_query(c, db, name, word):
    def insert_history():
        sql = "insert into history(time, name, word) values('%s','%s','%s')" % (time.ctime(), name, word)
        try:
            cursor.execute(sql)
        except:
            db.rollback()
            return
        db.commit()
    cursor = db.cursor()
    # nextw = chr(word.encode()[0] + 1)#获取大于要查单词的字母,查询不到的结束条件
    nextw = chr(ord(word[0]) + 1)
    sql = "select word,ipe from words where word='%s' and word<'%s'" % (word, nextw)
    try:
        cursor.execute(sql)
        result1 = cursor.fetchone()
        print(result1)
    except Exception:
        db.rollback()
        cursor.close()
        c.send('查询出现异常'.encode())
        return
    db.commit()
    if result1:
        result = ' '.join(result1)
        c.send(result.encode())
        insert_history()
    else:
        c.send('未找到这个单词'.encode())



def do_history(c, db, name):
    cursor = db.cursor()
    sql = "select word from history where name='%s' order by time desc limit 10" % name
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except:
        db.rollback()
        cursor.close()
        c.send('查询失败'.encode())
        return
    if data:
        result = ' '.join(map( lambda x: x[0], data))
        c.send(result.encode())
    else:
        c.send('没有历史记录'.encode())

if __name__ == "__main__":
    main()









