from socket import *
import sys
import getpass
import time

def main():
    s = socket()
    if len(sys.argv) < 3:
        return
    s.connect((sys.argv[1],int(sys.argv[2])))
    while True:
        print('===========菜单===========')
        print('---------１．注册---------')
        print('---------２．登录---------')
        print('---------３．退出---------')
        print('=========================')
        try:
            cmd = int(input('请输入数字:'))
        except ValueError:
            print('输入有误')
            sys.stdin.flush()
            continue
        if cmd in [1, 2]:
            p = Client(s)
            if cmd == 2:
                p.do_login()
            else:
                name = p.do_register()
                if name:
                    print('登录成功')            
                    p.login(s, name)
                else:
                    print('登录失败')
        elif cmd == 3:
            s.send(b'E')
            s.close()
            sys.exit('谢谢使用')
        else:
            print('输入有误')
            sys.stdin.flush()
class Client(object):
    def __init__(self, s):
        self.s = s
        self.list = []
    def do_register(self):
        while True:
            name = input('用户名：')
            if ' ' in name:
                print('名字中不能有空格')
                sys.stdin.flush()
                continue
            password = getpass.getpass('密码')
            password1 = getpass.getpass('确认密码')
            if (' ' in password) or (password != password1):
                sys.stdin.flush()
                print('输入有误')
                continue
            self.s.send('R {} {}'.format(name, password).encode())
            roll = self.s.recv(128).decode()
            if roll == 'OK':
                return name
            else:
                print(roll)
                return 0
    def do_login(self):
            name = input('用户名：')
            password = getpass.getpass('密码：')
            if ' ' in name or ' ' in password:
                print('用户名输入有误')
                return
            msg = 'L {} {}'.format(name, password)
            self.s.send(msg.encode())
            data = self.s.recv(128).decode()
            if data == 'OK':
                print('登录成功')
                self.login(name)
            else:
                print(data)


    def login(self, name):
        while True:
            print('''\n
            ===========查询界面============
            1.查词     2.历史记录   3.注销
            =============================
            ''')
            try:
                cmd = int(input("输入选项>>"))
            except Exception:
                print("命令错误")
                continue
            if cmd not in [1,2,3]:
                print("对不起，没有该命令")
                sys.stdin.flush() #清除输入
                continue 
            elif cmd == 1:
                self.do_query(name)
            elif cmd == 2:
                self.do_history(name)
            elif cmd == 3:
                return
    def do_query(self, name):
        while True:
            w = input('输入单词,输入##结束查询:')
            if w == '##':
                return
            msg = 'Q {} {}'.format(name, w)
            self.s.send(msg.encode())
            data = self.s.recv(1024).decode()
            if data == 'OK':
                data = self.s.recv(1024).decode().strip()
                # self.list.append((time.ctime(), w, data))
                print(data)
            else:
                print(data)

    def do_history(self, name):
        for s in self.list:
            print(s)


if __name__ == '__main__':
    main()




