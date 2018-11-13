
# TFTP文无服务器tcp－Thread
from socket import *
import os
from threading import Thread
import time
import sys

class MyTftp(object):

    def __init__(self,host,port):
        self.s = socket()
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((host,port))
        self.s.listen(5)
        self.static = "/home/tarena/static/"

    def show_menu(self, c):
        l = os.listdir(self.static)
        if not l:
            c.send("文件夹为空".encode())
            return
        c.send(b'OK')
        time.sleep(0.5)
        obj = "#".join(filter(lambda x:os.path.isfile(self.static + x),l))
        c.send(obj.encode())


    def get_file(self, c, filename):
        # if os.path.exists(self.static + filename):
        try:
            f = open(self.static + filename, "rb")
            c.send(b'OK')
            time.sleep(0.5)
            try:
                while True:
                    data = f.read(1024)
                    if data:
                        c.send(data)
                    else:
                        time.sleep(0.5)
                        c.send("$$".encode())
                        f.close()
                        break
        except Exception as e:
            print(e)
            c.send("文件打开失败".encode())



    def post_file(self, c, filename):
        try:
            f = open(filename,"wb")
            c.send(b'OK')
        except OSError:
            c.send("打开文件失败".encode())
        else:
            try:
                while True:
                    data = c.recv(1024)
                    if data == b'$$':
                        break
                    else:
                        f.write(data)
                f.close()
                c.send(b'OK')
            except Exception:
                c.send(b'False')

    def main(self):
        # 等待连接
        #多线程完成不同任务
        try:
            while True:
                c, addr = self.s.accept()
                print("connect{}".format(addr))
                c.send(b'OK')
                th = Thread(target=self.handler, args=(c,))
                th.setDaemon(True)
                th.start()
        except Exception as e:
            print(e)
            
    def handler(self, c):
        while True:
            data = c.recv(1024).decode().strip()
            print(data)
            if data:
                order = data.split(" ")[0]
                if order == "Q":
                    self.show_menu(c)
                elif order == "G":
                    filename = data.split(" ")[1]
                    self.get_file(c, filename)
                elif order == "P":
                    filename = data.split(" ")[1]
                    self.post_file(c, filename)
                elif order == "Z":
                    c.close()
                    sys.exit(0)
            else:
                c.close()



if __name__ == "__main__":
    MyTftp("127.0.0.1",8888).main()




# TFTP文无服务器tcp－Thread
# from socket import *
# import os
# from threading import Thread
# from multiprocessing import Process
# import time
# import sys

# class MyTftp(object):

#     def __init__(self,host,port):
#         self.s = socket()
#         self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#         self.s.bind((host,port))
#         self.s.listen(5)
#         self.static = "/home/tarena/static/"

#     def show_menu(self, c):
#         l = os.listdir(self.static)
#         if not l:
#             c.send("文件夹为空".encode())
#             return
#         c.send(b'OK')
#         time.sleep(0.5)
#         obj = "#".join(filter(lambda x:os.path.isfile(self.static + x),l))
#         c.send(obj.encode())


#     def get_file(self, c, filename):
#         # if os.path.exists(self.static + filename):
#         try:
#             f = open(self.static + filename, "rb")
#             c.send(b'OK')
#             time.sleep(0.5)
#             while True:
#                 data = f.read(1024)
#                 if data:
#                     c.send(data)
#                 else:
#                     time.sleep(0.5)
#                     c.send("$$".encode())
#                     f.close()
#                     break
#         except Exception as e:
#             print(e)
#             c.send("文件打开失败".encode())



#     def post_file(self, c, filename):
#         try:
#             f = open(self.static+filename,"wb")
#             c.send("OK".encode())
#         except OSError:
#             c.send("打开文件失败".encode())
#         else:
#             try:
#                 while True:
#                     data = c.recv(1024)
#                     if data == '$$'.encode():
#                         break
#                     else:
#                         f.write(data)
#                         continue
#                 f.close()
#                 c.send('上传成功'.encode())
#             except Exception:
#                 c.send(b'False')

#     def handler(self, c):
#         while True:
#             try:
#                 data = c.recv(1024).decode().strip()
#             except Exception as e:
#                 print(e)
#             if data:
#                 order = data.split(" ")[0]
#                 if order == "Q":
#                     self.show_menu(c)
#                 elif order == "G":
#                     filename = data.split(" ")[1]
#                     self.get_file(c, filename)
#                 elif order == "P":
#                     filename = data.split(" ")[1]
#                     print(filename)
#                     self.post_file(c, filename)
#                 elif order == "Z":
#                     c.close()
#                     sys.exit(0)
#             else:
#                 c.close()

#     def main(self):
#         # 等待连接
#         #多线程完成不同任务
#         try:
#             while True:
#                 c, addr = self.s.accept()
#                 print("connect{}".format(addr))
#                 c.send(b'OK')
#                 th = Process(target=self.handler, args=(c,))
#                 th.daemon = True
#                 th.start()
#         except Exception as e:
#             print(e)
            



# if __name__ == "__main__":
#     MyTftp("127.0.0.1",8888).main()

