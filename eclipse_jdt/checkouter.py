# -*- coding: utf-8 -*-
import re
import csv
import os.path
import os
import subprocess
import sys

"""
description:
assumed directory structure:    this script -> .
                                git repository of the target project -> ./
files and dirs required:        revision_(pjt name).csv
                                (pjt_name) <- git repository of the target project
files and dirs created:         files_main_(revision).txt
                                files_test_(revision).txt
                                linkdata(revision).txt
                                data_(pjt name)_(revision) <- directory
caller:                         auto_top.sh
callee:                         auto.sh
"""

pjt_name = "eclipse.jdt.core"
file_name = "eclipse_jdt"
f = open('revision_' + file_name + '.csv', 'r')
flag = 0
for info in f: # info = [Date, Revision]
    if flag == 0: # pass here only the first loop
        flag += 1
        continue
    date = info.split(',')[0]
    revision = info.split(',')[1]
    revision = revision.replace("\n", "")
    print date + " " + revision
    os.chdir('./'+pjt_name) # dive into the git repository
    subprocess.check_output("git checkout " + revision)
    os.chdir('..') # back from the git repository
    product_code_files = "files_main_" + revision + ".txt"
    test_code_files = "files_test_" + revision + ".txt"
    link_file = "linkdata" + revision + ".csv"
    dir_name = "data_" + pjt_name + "_" + revision
    subprocess.check_output("auto.sh " + product_code_files + " " + test_code_files + " " + link_file + " " + dir_name, shell=True)
    os.chdir('./'+pjt_name) # dive into the git repository
    subprocess.check_output("git checkout master")
    os.chdir('..') # back from the git repository
    sys.exit("execution abortion")
f.close()
