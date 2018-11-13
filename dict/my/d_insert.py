import re
import pymysql
import sys

try:
    f = open('dict.txt')
except OSError:
    sys.exit('文件打开失败')

db = pymysql.connect('localhost', 'root', '123456','dict')
cursor = db.cursor()
pattern = r"[ ]+"
for line in f:
    try:
        data = re.split(pattern, line)
        word = data[0]
        ipe = ' '.join(data[1:])
        sql = "insert into words(word, ipe) values('%s','%s');" % (word, ipe)
        cursor.execute(sql)
    except Exception as e:
        db.rollback()
        continue
    db.commit()
f.close()
cursor.close()
db.close()





