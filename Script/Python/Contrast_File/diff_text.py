'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   6/3/17 6:27 PM
'''
# !/usr/bin/env python3
# coding=utf-8

import sys, difflib

try:
    textfile1 = sys.argv[1]
    textfile2 = sys.argv[2]
    print("Diff", textfile1, textfile2)
except Exception as e:
    print("Error:", str(e))
    print("Usage: diff_text.py filename1 filename2")
    sys.exit()

def readfile(filename):
    try:
        fileHandle = open(filename, 'r')
        text = fileHandle.read().splitlines()
        fileHandle.close()
        return text
    except IOError as e:
        print("Read file Error:", str(e))
        sys.exit()

if textfile1=="" or textfile2=="":
    print("Usage: diff_text.py filename1 filename2")
    sys.exit()

text1_lines = readfile(textfile1)
text2_lines = readfile(textfile2)

hdiff = difflib.HtmlDiff().make_file(text1_lines, text2_lines)
print(hdiff)

# python3 diff_text.py filename1 filename2 > diff_text.html