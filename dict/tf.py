# #!/usr/bin/env python3
# #coding=utf-8
# import getpass
# user = getpass.getpass('-->')
# passwd = getpass.getpass('-->')
# print(user,passwd)

import gevent
#在socket导入之前导入
from gevent import monkey
monket.patch_all()
from socket import *
from time import ctime

def server(port):
    s = socket()
    s.bind(('0.0.0.0',port))
    s.listen(5)
    while True:
        c, addr = s.accept()
        handler()

def handler():
    pass


if __name__ == '__main__':
    server(8888)












