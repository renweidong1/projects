from socket import *
import sys

class DictClient(object):
    #创建套接字
    def __init__(self, addr):
        self.s = socket()
        self.addr = addr
    #处理登录
    def do_login(self):
        while True:
            name = input("请输入用户名(直接回车退出)：")
            if not name:
                return
            if ' ' in name:
                print("用户名错误")
                continue
            password = input("请输入密码:")
            if ' ' not in password:
                data = "L " + name + " " + password
                print(data)
                self.s.send(data.encode())
                result = self.s.recv(128).decode()
                if result == "OK":
                    return name
                print(result)
                continue

# 　　　　处理注册
    def do_register(self):
        name = input("请输入用户名：")
        if ' ' in name:
            print("用户名错误")
            return
        password = input("请输入密码:")
        password1 = input("请确认密码:")
        if ' ' not in password and password == password1:
            data = "R " + name + " " + password
            self.s.send(data.encode())
            result = self.s.recv(128).decode()
            if result == "OK":
                return name
            print(result)
            return 0

# 　　　　查询单词
    def querywords(self, name):
        while True:
            word = input("请输入单词(直接回车结束):")
            if not word:
                break
            msg = "C " + name + " " + word
            self.s.send(msg.encode())
            data = self.s.recv(1024).decode()
            if data == "no":
                print("没有该单词")
                continue
            data = data.split("#")
            print(data[0]+" " * 5 + data[1])
    # 查询历史记录
    def queryhistory(self, name):
        msg = "H " + name
        self.s.send(msg.encode())
        while True:
            data = self.s.recv(1024).decode()
            if data == "none":
                print("没有历史记录")
                return
            if data == "##":
                break
            print(data)

        
        # 二级界面
    def second_menu(self,name):
        while True:
            print("===================")
            print("-------1.查词-------")
            print("-------2.历史-------")
            print("-------q.退出-------")
            print("===================")
            msg = input("请输入命令：").strip()
            if msg not in ['1', '2', 'q']:
                print("输入正确命令")
                continue
            if msg == "1":
                self.querywords(name)
            elif msg == "2":
                self.queryhistory(name)
            else:
                return
# 　　　　连接和界面显示 
    def main(self):
        try:
            self.s.connect(self.addr)
        except Exception as e:
            self.s.close()
            sys.exit(e)
        else:
            while True:
                print("===================")
                print("-------1.登录-------")
                print("-------2.注册-------")
                print("-------q.退出-------")
                print("===================")
                msg = input("请输入命令：").strip()
                if msg not in ['1', '2', 'q']:
                    print("输入正确命令")
                    continue
                if msg == "1":
                    name = self.do_login()
                    if name:
                        self.second_menu(name)
                elif msg == "2":
                    name = self.do_register()
                    if name:
                        print("注册成功")
                        self.second_menu(name)
                else:
                    self.s.close()
                    sys.exit("谢谢使用")



if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("输入错误")
    host = sys.argv[1]
    port = int(sys.argv[2])
    addr = (host,port)
    DictClient(addr).main()

