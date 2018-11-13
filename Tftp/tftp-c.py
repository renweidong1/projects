from socket import *
import sys
import time
import csv


class TftpClient(object):
    def __init__(self, addr):
        self.s = socket()
    def get_menu(self):
        self.s.send(b'Q')
        data = self.s.recv(1024).decode()
        if data == "OK":
            data = self.s.recv(1024).decode()
            self.data_list = data.split("#")
            print(self.data_list)
            with open("menu.csv","wt") as f:
                cv = csv.writer(f)
                for x, y in enumerate(self.data_list):
                    cv.writerow([x, y])
                print("OK")
        else:
            print(data)

    def get_file(self):
        msg = input("请输入文件名：").strip()
        if msg not in self.data_list:
            print("文件不存在")
            return
        else:
            msg = msg.encode()
            sev = b'G ' + msg
            self.s.send(sev)
            data = self.s.recv(124).decode()
            if data == "OK":
                with open(msg,'wb') as f:
                    while True:
                        data = self.s.recv(1024)
                        if data == "$$".encode():
                            print("下载完成")
                            break
                        else:
                            f.write(data)
            else:
                print(data)


    def post_file(self):
        filename = input("输入文件名:").strip()
        try:
            f = open(filename, 'rb')
        except OSError:
            print("打开文件失败")
        else:
            filename = filename.encode()
            msg = b'P ' + filename
            self.s.send(msg)
            data = self.s.recv(1024).decode()
            if data == "OK":
                while True:
                    data = f.read(1024)
                    if data:
                        self.s.send(data)
                    else:
                        time.sleep(1)
                        self.s.send("$$".encode())
                        f.close()
                        break
                result = self.s.recv(1024).decode()
                print(result)
            else:
                print(data)
                return

    def main(self):
        try:
            self.s.connect(addr)
            data = self.s.recv(1024).decode()
            print(data)
        except Exception as e:
            print(e)
        while True:
            print("==========menu==========")
            print("-------1.get menu-------")
            print("-------2.get file-------")
            print("-------3.post file------")
            print("-------q.quit-----------")
            print("========================")
            try:
                msg = input("请输入选项：").strip()
                if msg == "1":
                    self.get_menu()
                elif msg == "2":
                    self.get_file()
                elif msg == "3":
                    self.post_file()
                elif msg == 'q':
                    self.s.send(b'Z')
                    self.s.close()
                    sys.exit("谢谢使用")
                else:
                    print("输入有误")
            except KeyboardInterrupt:
                    self.s.send(b'Z')
                    self.s.close()
                    sys.exit("谢谢使用")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("输入有误")
    host = sys.argv[1]
    port = int(sys.argv[2])
    addr = (host,port)
    TftpClient(addr).main()
