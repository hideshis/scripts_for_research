# -*- coding: utf-8 -*-
"""
this script identifies buggy files.
you have to the full path of the SZZnized git repo before execution.
input:  SZZnized git repo.
output: buggy_file_list.txt
        tag_list.txt
        tag_list_bug.txt
"""

import os
import sys
import subprocess
import csv

def buggy_file_list_getter(tag):
    result = subprocess.check_output('git show --name-only --date=raw ' + tag, shell=True)
    result = result.replace('\r', '')
    tag_info_list = result.split('\n')
    author_flag = 0
    for tag_info in tag_info_list:
        if tag_info.startswith("@@") and tag_info.endswith("@@@@"):
            tag_info = tag_info[2:-4] # remove redundant @s
            buggy_file_list = tag_info.split("@@")
            for buggy_file in buggy_file_list:
                os.system('echo ' + buggy_file + '>>buggy_file_list.txt')
        if tag_info.startswith('Author: '):
            author_flag = 1
        if (author_flag == 1) and (tag_info.startswith('Date:   ')):
            bugged_time = tag_info.split(' ')[-2]
            break
    writer = csv.writer(file('buggy_file_info.csv', 'a'), lineterminator="\n")
    for buggy_file in buggy_file_list:
        info_list = []
        info_list.append(bugged_time)
        info_list.append(buggy_file)
        writer.writerow(info_list)
    return


home_path = os.path.abspath(os.path.dirname(__file__))
repo_path = '/Users/hideshi-s/Desktop/exp/result/15/0626seminar2/httpclient/original.git'
os.chdir(repo_path)
os.system('git tag > tag_list.txt')
os.system('egrep -e "^_BUG-" tag_list.txt > tag_list_bug.txt')
allLines = open('tag_list_bug.txt').read()
allLines = allLines.replace('\r', '')
tag_list = allLines.split('\n')
tag_list.pop()
for tag in tag_list:
    buggy_file_list_getter(tag)
os.system('mv buggy_file_list.txt ' + home_path)
os.system('mv tag_list.txt ' + home_path)
os.system('mv tag_list_bug.txt ' + home_path)
os.system('mv buggy_file_info.csv ' + home_path)
