from socket import *
import sys
import getpass

def main():
    s = socket()
    if len(sys.argv) < 3:
        print('请输入地址')
        return
    ADDR = (sys.argv[1],int(sys.argv[2]))
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e)
        return
    while True:
        print('''
        ==========菜单==========
        1.注册   2.登录   3.退出
        ========================''')
        try:
            digit = int(input('请输入数字：'))
        except Exception as e:
            print('输入有误')
            continue
        if digit == 1:
            d = do_register(s)
            if d:
                login(s, d)
            else:
                continue
        elif digit == 2:
            d = do_login(s)
            if d:
                login(s, d)
            else:
                continue           

        elif digit == 3:
            s.send(b'E')
            sys.exit('谢谢使用')   
        else:
            print('请输入正确命令')
            sys.stdin.flush()
            continue

def do_register(s):
    name = input('请输入用户名:')
    password = input('请输入密码:')
    password1 = input('请确认密码:')
    if (' ' in name) or (' ' in password):
        print('输入有误，请重新输入')
        sys.stdin.flush()
        return
    elif password != password1:
        print('输入密码不一致')
        sys.stdin.flush()
        return
    msg = 'R {} {}'.format(name, password)
    try:
        s.send(msg.encode())
    except Exception:
        print('注册异常')
        return 0
    data = s.recv(128).decode()
    if data == 'OK':
        print('注册成功,直接登录！')
        return name
    else:
        print(data)
        return 0

def do_login(s):
    name = input('请输入用户名：')
    password = getpass.getpass('请输入密码:')
    if ' ' in (name or password):
        print('用户名或密码输入格式错误')
        sys.stdin.flush()
        return
    s.send('L {} {}'.format(name, password).encode())
    data = s.recv(1024).decode()
    if data == 'OK':
        print('登录成功')
        return name
    else:
        print(data)
        return 0

def login(s, name):
    while True:
        print('''\n
        =========查询界面=========
        1.查词  2.历史记录  3.注销
        ==========================
        ''')
        try:
            msg = int(input('请输入数字：'))
        except ValueError:
            print('输入有误')
            continue
        if msg not in [1, 2, 3]:
            print('请输入正确命令')
            continue
        elif msg == 1:
            do_query(s, name)
        elif msg == 2:
            do_history(s, name)
        elif msg == 3:
            return
def do_query(s, name):
    while True:
        word = input('查词（输入q结束）：')
        if word == 'q':
            return
        msg = 'Q {} {}'.format(name, word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        print(data)

def do_history(s, name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data[0].isalpha():
        for x in data.split(' '):
            print(x)
    else:
        print(data)
if __name__ == "__main__":
    main()





    






