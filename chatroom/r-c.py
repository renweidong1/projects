from socket import *
import os
import sys
import signal

if len(sys.argv) < 3:
    sys.exit("登录失败")
host = sys.argv[1]
port = int(sys.argv[2])

class ChatClient(object):
    def __init__(self, host, port):
        self.s = socket(AF_INET,SOCK_DGRAM)
        self.addr = ((host,port))

    def do_sendto(self, name):
        while True:
            try:
                msg = input()
            except KeyboardInterrupt:
                data = 'Q ' + name + " "
                self.s.sendto(data.encode(), self.addr)
                self.s.close()
                sys.exit("退出聊天室")
            if msg == '':
                data = 'Q ' + name + " "
                self.s.sendto(data.encode(), self.addr)
                self.s.close()
                sys.exit("退出聊天室")
            msg = "S "+ name +" "+ msg
            self.s.sendto(msg.encode(),self.addr)
    def do_recvfrom(self):
        while True:
            try:
                data, addr = self.s.recvfrom(1024)
                print("\r" + data.decode())
                print("\r请发言>>",end="")
            except:
                sys.exit(0)
    def main(self):
        name = input("input your name:")
        self.s.sendto(("L "+name + " ").encode(),self.addr)
        data, addr = self.s.recvfrom(1024)
        data = data.decode()
        # signal.signal(signal.SIGCHLD,signal.SIG_IGN)
        print(data)
        if data == '登录成功':
            print("\r请发言>>",end="")
            pid = os.fork()
            if pid == 0:
                self.do_sendto(name)
            elif pid > 0:
                self.do_recvfrom()
                os.wait()
            else:
                sys.exit("进程创建失败")



if __name__ == "__main__":
    ChatClient(host,port).main()















