'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 9:18
'''
# !/usr/bin/env python3
# coding=utf-8

import difflib

text1 = """text1:
This is hello world!
Google"""
text2 = """text2:
This is Hello World~
gOoOgle"""

text1_lines = text1.splitlines()
text2_lines = text2.splitlines()

# diff = difflib.Differ().compare(text1_lines, text2_lines)
# print('\n'.join(list(diff)))

hdiff = difflib.HtmlDiff().make_file(text1_lines, text2_lines)
print(hdiff)

# python3 diff_string.py > diff_string.html