# -*- coding: utf-8 -*-
"""
this script formats imported_pc_list.csv

input: imported_pc_list.csv
output: imported_pc_list_formatted.csv
"""

import sys
import os
import subprocess
import csv

f = open("result.csv", "r")
os.system('egrep "^Commit_hash," change_history_view.csv >> change_history_view_drip.csv')
dataReader = csv.reader(f)
for line in dataReader:
    commit_hash = line[0]
    os.system('egrep "^' + commit_hash + '" change_history_view.csv >> change_history_view_drip.csv')
