# -*- coding: utf-8 -*-
"""
"""

import os
import sys
import subprocess
import csv

def buggy_file_list_getter(tag):
    result = subprocess.check_output('git show --name-only ' + tag, shell=True)
    result = result.replace('\r', '')
    tag_info_list = result.split('\n')
    for tag_info in tag_info_list:
        if tag_info.startswith("@@") and tag_info.endswith("@@@@"):
            tag_info = tag_info[2:-4] # remove redundant @s
            buggy_file_list = tag_info.split("@@")
            break
    return buggy_file_list


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
    buggy_file_list = buggy_file_list_getter(tag)
    for buggy_file in buggy_file_list:
        os.system('echo ' + buggy_file + '>>buggy_file_list.txt')
os.system('mv buggy_file_list.txt ' + home_path)
os.system('mv tag_list.txt ' + home_path)
os.system('mv tag_list_bug.txt ' + home_path)
