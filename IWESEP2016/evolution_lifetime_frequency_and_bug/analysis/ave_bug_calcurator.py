# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

def ave_bug_calcurator(csv_file):
    result = subprocess.check_output('cat ' + csv_file + ' | cut -d, -f6', shell=True)
    result = result.replace("\r", "")
    num_bug_list = result.split("\n")
    del num_bug_list[-1]
    bug_counter = 0
    for num_bug in num_bug_list:
        bug_counter += float(num_bug)
    ave_bug = float(bug_counter) / len(num_bug_list)
    print csv_file, str(ave_bug), str(bug_counter), len(num_bug_list)
    return

csv_list = os.listdir("./")
for csv_file in csv_list:
    if not csv_file.endswith(".csv"):
        continue
    ave_bug_calcurator(csv_file)
