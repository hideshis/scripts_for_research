# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import csv
import re

"""
This script identifies buggy files and lines and the revision which the bug was injected.
"""

def tag_list_getter(git_repo_path, script_path): # obtain the list of tags. Each tag indicates the revision which the bug was injected.
    os.chdir(git_repo_path)
    result = subprocess.check_output('git tag | grep "^_BUG"', shell=True)
    result = result.replace('\r', '')
    tag_list = result.split('\n')
    tag_list.pop()
    os.chdir(script_path)
    return tag_list

def buggy_file_list_getter_sub(buggy_file_candidate_list, tag):
    buggy_file_list = []
    for buggy_file_candidate in buggy_file_candidate_list:
        try:
            cmd = 'git show --pretty=format:"" --name-only ' + tag + ' | grep -v "@@@@" | grep "' + buggy_file_candidate + '"'
            result = subprocess.check_output(cmd, shell=True)
            result = result.replace("\r", "")
            result_list = result.split("\n")
            result_list.pop()
            buggy_file_list.append(result_list[0])
        except subprocess.CalledProcessError:
            continue
    return buggy_file_list

def buggy_file_list_getter(git_repo_path, script_path, tag): # obtain the list of buggy files.
    os.chdir(git_repo_path)
    buggy_file_str = subprocess.check_output('git show --pretty=format:"" --name-only ' + tag + ' | egrep "^@@.+@@@@$"', shell=True)
    buggy_file_str = buggy_file_str.replace('\r', '').replace('\n', '')
    buggy_file_str = buggy_file_str[2:-4]
    # @@~~~~@@@@内のファイル群全てが，このコミットで変更されたとは限らない．
    buggy_file_list = buggy_file_list_getter_sub(buggy_file_str.split("@@"), tag)
    os.chdir(script_path)
    return buggy_file_list

def buggy_area_list_getter(git_repo_path, script_path, tag, buggy_file):
    os.chdir(git_repo_path)
    cmd = 'git log -n 1 -p ' + tag + ' -- ' + buggy_file + ' | grep "^@@ -"'
    result = subprocess.check_output(cmd, shell=True)
    result_list = result.split('\n')
    result_list.pop()
    buggy_area_list = []
    for var in result_list: # ex) var="@@ -113,9 +113,10 @@ dependencyManagement_tag = 'dependencyManagement'" / in "-L1,R1 +L2,R2", +L2,R2 means bug-injected line (L2) and range (R2)
        buggy_area_str = var.split(' ')[2][1:] # ex) var.split(' ')[2]='+113,10', buggy_area_str='113,10'
        start_line = int(buggy_area_str.split(',')[0]) # ex) start_line=113
        end_line = start_line + int(buggy_area_str.split(',')[1]) # end_line=113+10=123
        buggy_area = [start_line, end_line]
        buggy_area_list.extend(buggy_area)
    os.chdir(script_path)
    return buggy_area_list

def buggy_area_getter(buggy_area_list):
    i = iter(buggy_area_list)
    while 1:
        yield i.next(), i.next()

git_repo_path = '/Users/hideshi-s/Desktop/exp/result/15/0626seminar2/httpclient/original.git'
script_path = os.path.abspath(os.path.dirname(__file__))
tag_list = tag_list_getter(git_repo_path, script_path)
f = open('bug_location_info.csv', 'w')
csvWriter = csv.writer(f, lineterminator='\n')
for tag in tag_list:
    # 変更されたファイルの取得 (tag に付与されたメッセージから)
    buggy_file_list = buggy_file_list_getter(git_repo_path, script_path, tag)
    for buggy_file in buggy_file_list:
        # diff の取得 (git log を使う)
        # バグが混入した箇所を取得するs
        buggy_area_list = buggy_area_list_getter(git_repo_path, script_path, tag, buggy_file)
        for start, end in buggy_area_getter(buggy_area_list):
            bug_info = [buggy_file, start, end, tag]
            csvWriter.writerow(bug_info)
f.close()
