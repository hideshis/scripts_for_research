# -*- coding: utf-8 -*-
"""
description:                    PC と TC のリンク情報を作製するスクリプト．
                                argvs[1]: PC のファイル名のリスト
                                argvs[2]: TC のファイル名のリスト
                                argvs[3]: PC と TC のリンク情報をまとめたcsvファイル
assumed directory structure:    this script -> .
                                directory of the target project -> (full path)/
files and dirs required:        (argvs[1])
                                (argvs[2])
files and dirs created:         (argvs[3])
caller:                         auto.sh
callee:                         none
"""
import os
import sys
import csv

argvs = sys.argv
f_main = open(argvs[1], "r")
f_link = csv.writer(file(argvs[3], "w"), lineterminator="\n")

id = 1
for main_file in f_main:
    csv_list = []
    main_file = main_file.replace("\n", "") # ファイル名の末尾が改行文字になっているので，除去する．
    csv_list.append(main_file)
    main_file = main_file.split(".")[0] # hoge.java が hoge になるようにする．
    print main_file
    f_test = open(argvs[2], "r")
    for test_file in f_test:
        test_file = test_file.replace("\n", "") # ファイル名の末尾が改行文字になっているので，除去する．
        test_file_copy = test_file
        test_file = test_file.split(".")[0] # hoge.java が hoge になるようにする．
        # test_file が main_file + (Test|test|TEST) ならば，test_file は main_file のテストコードであると判定する．
        if test_file == (main_file + "Test") or test_file == (main_file + "test") or test_file == (main_file + "TEST"):
            csv_list.append(test_file_copy)
            break
    f_test.close()
    # プロダクトコードに対するテストコードが存在しなかった場合，テストコード名の欄には none と記載する．
    if len(csv_list) == 1:
        csv_list.append("none")
    #csv_list.append(id)
    f_link.writerow(csv_list)
    id += 1
f_main.close()
