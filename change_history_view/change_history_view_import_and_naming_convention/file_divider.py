# -*- coding: utf-8 -*-
"""
this script splits the execution into peaces.

input: (pjt_name)_tc.csv
output: process(num).csv
"""

import sys
import subprocess
import os

def file_divider(pjt_name, start, end):
    cmd = 'sed -n -e ' + str(start) +',' + str(end) + 'p ' + pjt_name + '_tc.csv'
    result = subprocess.check_output(cmd, shell=True)
    f = open("tmp" + str(end) + ".csv", "w")
    f.write(result)
    f.close()
    cmd = 'mkdir process' + str(end)
    os.system(cmd)
    cmd = 'cp *.py process' + str(end)
    os.system(cmd)
    cmd = 'cp *.txt process' + str(end)
    os.system(cmd)
    cmd = 'cp *.csv process' + str(end)
    os.system(cmd)
    os.chdir('./process' + str(end))
    cmd = 'rm ' + pjt_name + '_tc.csv'
    os.system(cmd)
    cmd = 'mv tmp' + str(end) + '.csv ' + pjt_name + '_tc.csv'
    os.system(cmd)
    os.chdir('..')
    os.system("rm tmp*.csv")
    return

argvs = sys.argv
pjt_name = argvs[1]
cmd = 'cat ' + pjt_name + '_tc.csv | wc -l'
num = subprocess.check_output(cmd, shell=True)
num = num.replace(" ", "")
num = num.replace("\n", "")
for x in range(int(num) + 1):
    if x % 1000 == 0:
        if x == 0:
            start = x + 1
        else:
            end = x
            file_divider(pjt_name, start, end)
            start = end + 1
if start < int(num):
    end = int(num)
    file_divider(pjt_name, start, end)
