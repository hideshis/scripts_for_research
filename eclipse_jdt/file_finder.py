# -*- coding: utf-8 -*-
"""
description:                    指定されたディレクトリとそのサブディレクトリを巡回し，
                                保存されているファイルの名前を抽出するスクリプト．
                                argvs[1]: 検索対象ディレクトリの絶対パス(エスケープを避けるため，パスの区切りはヌル文字ではなくスラッシュにすること．)
                                argvs[2]: プロダクトコードのファイル名のリストを格納するファイルの名前．
                                argvs[3]: テストコードのファイル名のリストを格納するファイルの名前．
assumed directory structure:    this script -> .
                                directory of the target project -> (full path)/
files and dirs required:        directory of the target project
files and dirs created:         (argvs[2]) <- list of product code
                                (argvs[3]) <- list of test code
caller:                         auto.sh
callee:                         none
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
            file_path_list = file.split("/")
            test_flag = 0
            for file_path in file_path_list:
                if ("test" in file_path) or ("Test" in file_path) or ("TEST" in file_path):
                    file = file.split('/')[-1]
                    f_test.write(file+"\n")
                    test_flag = 1
                    break
            if test_flag == 0:
                file = file.split('/')[-1]
                f_product.write(file+"\n")
            print file
f_product.close()
f_test.close()
