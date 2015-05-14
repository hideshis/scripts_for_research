# -*- coding: utf-8 -*-
"""
PC と TC のリンク情報を作製するスクリプト．
argvs[1]: PC のファイル名のリスト
argvs[2]: TC のファイル名のリスト
argvs[3]: PC と TC のリンク情報をまとめたcsvファイル
"""
import os
import sys
import csv

argvs = sys.argv
f_query = open(argvs[1], "r")
f_writer = csv.writer(file(argvs[3], "w"), lineterminator="\n")
f_writer.writerow(['Date', 'Author', 'ID', 'Sort'])

flag = 0
new_file_list = []
f_answer = open(argvs[2], "r")
id_counter = 1
for answer in f_answer:
    id_counter += 1
id_counter += 1

for query in f_query:
    if flag == 0:
        flag = 1
        continue
    csv_list = []
    query = query.replace("\n", "") # ファイル名の末尾が改行文字になっているので，除去する．
    query_list = query.split(',')
    csv_list.append(query_list[0])
    csv_list.append(query_list[1])
    f_answer = open(argvs[2], "r")
    for answer in f_answer:
        answer = answer.replace("\n", "") # ファイル名の末尾が改行文字になっているので，除去する．
        answer_list = answer.split(',')
        if query_list[2] == answer_list[0]:
            csv_list.append(answer_list[2])
            csv_list.append("P")
            break;
        elif query_list[2] == answer_list[1]:
            csv_list.append(answer_list[2])
            csv_list.append("T")
            break;
    f_answer.close()
    if len(csv_list) == 2:
        if not (query_list[2] in new_file_list):
            new_file_list.append(query_list[2])
        csv_list.append(id_counter + new_file_list.index(query_list[2]))
        if ("test." in query_list[2]) or ("Test." in query_list[2]) or ("TEST." in query_list[2]):
            csv_list.append("T")
        else:
            csv_list.append("P")
    f_writer.writerow(csv_list)
f_query.close()
