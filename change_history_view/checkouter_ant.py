# -*- coding: utf-8 -*-
import re
import csv
import os.path
import os
import subprocess
import sys

filename = "ant"
start_date = "20061026"
end_date = "20140831"
f = open('revision_' + filename + '.csv', 'r')
flag = 0
for info in f:
    if flag == 0:
        flag += 1
        continue
    date = info.split(',')[0]
    revision = info.split(',')[1]
    revision = revision.replace("\n", "")
    if (start_date <= date) and (date <= end_date):
        print date + " " + revision
        os.chdir('./'+filename)
        subprocess.check_output("git checkout " + revision)
        os.chdir('..')
        product_code_files = "files_main_checkstyle" + revision + ".txt"
        test_code_files = "files_test_checkstyle" + revision + ".txt"
        link_file = "linkdata" + revision + ".csv"
        dir_name = "data_" + filename + "_" + revision
        subprocess.check_output("auto.sh " + product_code_files + " " + test_code_files + " " + link_file + " " + dir_name, shell=True)
        os.chdir('./'+filename)
        #subprocess.check_output("git checkout master")
        os.chdir('..')
        print "\n\n" + str(flag) + "/2001 finished"
        flag += 1
f.close()
