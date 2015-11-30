# -*- coding: utf-8 -*-
"""
"""

import os
import sys
import subprocess
import csv

def bug_containing_file_list_getter():
    bug_containing_file_list = []
    f = open("tag_info.txt", "r")
    line = f.readline()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    while line and (not line == ""):
        if line.endswith(".java"):
            os.system('echo ' + line + '>>bug_containing_file_list.txt')
        line = f.readline()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
    f.close()
    return

f = open("tag_fix.txt", "r")
line = f.readline()
tag = line.replace("\r", "")
tag = tag.replace("\n", "")
while tag:
    os.chdir("./httpclient/original.git")
    os.system('git show --name-only ' + tag + ' | tail -r > tag_info.txt')
    os.system('mv tag_info.txt ../..')
    os.chdir("../..")
    bug_containing_file_list_getter()
    line = f.readline()
    tag = line.replace("\r", "")
    tag = tag.replace("\n", "")
f.close()
