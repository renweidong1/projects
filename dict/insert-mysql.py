import re
import pymysql
import sys
import time

class InsertMysql(object):

    def __init__(self):
        self.db = pymysql.connect("localhost",'root','123456',"dict",charset="utf8")
        self.cursor = self.db.cursor()

    def insert_info(self):
        try:
            f = open("dict.txt")
        except OSError as e:
            sys.exit("文件打开失败")
        insert = "insert into words(word,interpreter) values(%s,%s)"
        while True:
            data = f.readline().strip()
            if not data:
                break
            pattern = r"[ ]{2,}"
            res = re.split(pattern, data)
            try:
                l = [res[0],"".join(res[1:])]
            except Exception:
                print(1)
            # time.sleep(0.6)
            # if len(l) != 2:
            #     print(l)
            try:
                self.cursor.execute(insert, l)
            except Exception as e:
                self.db.rollback()
            else:
                self.db.commit()
        print("OK")

    def main(self):
        self.insert_info()

if __name__ == "__main__":
    InsertMysql().main()

