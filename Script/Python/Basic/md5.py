# coding=utf-8

'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/10/10 09:36
'''

import os
import hashlib

# 对字符串计算 md5
def Get_Md5_Of_String(src):
    md1 =hashlib.md5()
    md1.update(src)
    return md1.hexdigest()

# 对文件计算 md5
def Get_Md5_Of_File(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

# 对文件夹计算 md5  递归计算目录下每个文件的md5值，写入 tmp.md5 再计算 tmp.md5 的 md5 值
def Get_Md5_Of_Folder(dir):
  MD5File = "tmp.md5"
  outfile = open(MD5File, 'w')
  for root, subdirs, files in os.walk(dir):
    for file in files:
      filefullpath = os.path.join(root, file)
      filerelpath = os.path.relpath(filefullpath, dir)
      md5 = Get_Md5_Of_File(filefullpath)
      outfile.write(md5)
  outfile.close()
  return Get_Md5_Of_File(MD5File)

print(Get_Md5_Of_Folder(os.getcwd()))