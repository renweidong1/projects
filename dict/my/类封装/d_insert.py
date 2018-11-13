import re
import pymysql
import sys
db = pymysql.connect('localhost', 'root', '123456', 'dict')
cursor = db.cursor()
# # pattern = r'^([a-z]+)\s{2,}(.+)'
# # pattern = r'^([a-zA-Z]+)\s{2,}(.+)'
# pattern = "[ ]+"
# try:
#     file = open('dict.txt')
# except Exception as e:
#     print(e)
#     sys.exit()
# for f in file:
#     try:
#         # data = re.search(pattern, f)
#         # word = data.group(1)
#         # ipe = data.group(2)
#         l = re.split(pattern, f)
#         word = l[0]
#         ipe = ' '.join(l[1:])
#     except Exception:
#         continue
#     sql = "insert into words(word, ipe) values('%s','%s')"%(word, ipe)
#     try:
#         cursor.execute(sql)
#     except Exception:
#         db.rollback()
#     db.commit()
# file.close()
# cursor.close()
# db.close()

data = cursor.execute('select * from words')#返回查询结果个数
db.commit()
cursor.close()
db.close()
print(data)





#regex复习：
# a = '123111qwe45htrtyrrr5464'
# pattern = r'(?P<dog>[a-z]+)r'
# l = re.split(pattern, a)
# print(l)
# regex = re.compile(pattern)
# print(regex.split(a))
# l = re.sub(pattern,'999',a)
# l = re.subn(pattern,'999',a)
# print(l)
# #regex属性：
# print(regex.groups)
# print(regex.groupindex)
# print(regex.pattern)
# print(regex.flags)

# print(re.findall(pattern, a))#默认匹配最长的
#返回match对象
# d = re.finditer(pattern, a)
# print(d)
# for x in d:
#     print(x.group(1))
#     print(x.group(),'---')

# d = re.match('(\d+)1',a)
# print(d.group(),d.group(1))

# d = re.fullmatch('(\d+)1.+',a)
# print(d.group(),d.group(1))

# d = re.search('(\d+)(\w+)',a)
# print(d.group(),d.group(1),d.group(2))



# a = '-12 12% 1/2 6.7 7.88 -5.5'
# pattern = r'-?\d+\.?/?%?\d*'
# print(re.findall(pattern,a))









