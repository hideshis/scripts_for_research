# -*- coding: utf-8 -*-
"""
指定されたディレクトリとそのサブディレクトリを巡回し，
保存されているファイルの名前を抽出するスクリプト．
argvs[1]: 検索対象ディレクトリの絶対パス(エスケープを避けるため，パスの区切りはヌル文字ではなくスラッシュにすること．)
argvs[2]: ファイル名のリストを格納するファイルの名前．
"""
import os
import sys

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

argvs = sys.argv
f_product = open(argvs[2], "w")
f_test = open(argvs[3], "w")
for file in fild_all_files(argvs[1]):
	if '.' in file: # ディレクトリ名を省き，ファイル名だけが抽出されるようフィルタリングする．
            file = file.replace('\\', '/')
            #file = file.split('/')[-1]
            #if ("test" in file) or ("Test" in file) or ("TEST" in file):
            if file.startswith("C:/Users/hideshi/git/ant/src/tests") or file.startswith("C:/Users/hideshi/git/ant/src/testcases"):
                file = file.split('/')[-1]
                f_test.write(file+"\n")
            #else:
            elif file.startswith("C:/Users/hideshi/git/ant/src/main"):
                file = file.split('/')[-1]
                f_product.write(file+"\n")
            print file
f_product.close()
f_test.close()
