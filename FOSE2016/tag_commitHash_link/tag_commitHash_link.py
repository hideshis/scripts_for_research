# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import csv

git_repo_path = '/Users/hideshi-s/Desktop/exp/result/15/0626seminar2/httpclient/original.git'
output_file_path = '/Users/hideshi-s/Desktop/scripts_for_research/FOSE2016/tag_commitHash_link/tag_commitHash_link.csv'
os.system('rm ' + output_file_path)
os.chdir(git_repo_path)
result = subprocess.check_output('git show-ref --tags | grep "_BUG"', shell=True)
result = result.replace('\r', '')
result = result.replace('refs/tags/', '')
result = result.replace(' ', ',')
for line in result.split('\n'):
    os.system('echo ' + line + '>> ' + output_file_path)
