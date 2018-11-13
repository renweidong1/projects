from socket import *
from multiprocessing import Process
import pymysql
import signal
import os

class ChatServer(object):

    def __init__(self,ADDR):
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.s.bind(ADDR)
        self.l = []

        self.db = pymysql.connect("127.0.0.1",'root',"123456",db="chatroom",charset="utf8")
        self.cursor = self.db.cursor()

    def do_login(self, name1, addr):
        try:
            sel = "select name from user where name=%s"
            name = self.cursor.execute(sel,[name1])
            if name:
                self.s.sendto('用户已存在'.encode(),addr)
                self.s.close()
                return False
            else:
                print("欢迎{}加入聊天室，IP为{}".format(name1,addr))
                ins = "insert into user(name) values(%s)"
                self.cursor.execute(ins,[name1])
                self.db.commit()
                self.s.sendto('登录成功'.encode(),addr)
                for x in self.l:
                    self.s.sendto("欢迎{}加入聊天室".format(name1).encode(),x)
                return True
        except Exception as e:
            print(e)
            self.s.sendto("登录失败".encode(),addr)
            self.s.close()

    def do_logout(self, name):
        data = name + "退出聊天室"
        print(data)
        for l in self.l:
            self.s.sendto(data.encode(),l)
        dele = "delete from user where name=%s"
        self.cursor.execute(dele,[name])
        self.db.commit()

    def do_child(self, name, content):
        data = name + "说：" + content
        print(data)
        print("管理员>>",end = "")
        print("\r",end="")

        for l in self.l:
            self.s.sendto(data.encode(),l)

    def se_chat(self,addr):
        while True:
            msg = input()
            data ="S 管理员 " + msg
            self.s.sendto(data.encode(),addr)

    def do_chat(self):
        while True:
            try:
                data, addr = self.s.recvfrom(1024)
                if not data:
                    self.l.remove(addr)             
            except OSError:
                print("客户端断开连接")
            else:
                data = data.decode().strip()
                msg = data.split(" ")[0]
                name = data.split(" ")[1]
                content = "".join(data.split(" ")[2:])
                if msg == "L":
                    if self.do_login(name, addr):
                        self.l.append(addr)
                elif msg == "Q":
                    self.do_logout(name)
                    self.l.remove(addr)
                elif msg == "S":
                    self.do_child(name, content)


    def main(self):
        # signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        # p1 = Process(target=self.do_chat)
        # addr = (host,port)
        # p2 = Process(target=self.se_chat,args=(addr,))
        # p1.start()
        # p2.start()
        pid = os.fork()
        if pid == 0:
            self.do_chat()
        elif pid > 0:
            self.se_chat((host,port))
            os.wait()



if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    ChatServer((host,port)).main()

