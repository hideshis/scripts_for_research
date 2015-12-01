# -*- coding: utf-8 -*-
"""
this script counts # of buggy files from the group of tested product codes.
this script also counts # of buggy files from the group of not-tested product codes.
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
import numpy
import matplotlib.pyplot as plt

def buggy_file_counter(file_name):
    allLines = open(file_name).read()
    allLines = allLines.replace('\r', '')
    pc_list = allLines.split('\n')
    pc_list.pop()
    buggy_file_list = []
    for pc in pc_list:
        result = subprocess.check_output('egrep "^' + pc + '" buggy_file_list.txt | wc -l', shell=True)
        result = result.replace('\n', '')
        buggy_file_list.append(int(result.split(" ")[-1]))
    print file_name
    print sum(buggy_file_list)
    print float(sum(buggy_file_list)) / len(buggy_file_list)
    data = numpy.array(buggy_file_list)
    print numpy.median(data)
    plt.hist(data)
    plt.savefig(file_name.replace(".txt", "") + ".png")
    return

buggy_file_counter('pc_with_test_list.txt')
buggy_file_counter('pc_without_test_list.txt')
