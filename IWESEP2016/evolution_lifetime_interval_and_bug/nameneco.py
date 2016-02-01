# -*- coding: utf-8 -*-
"""
dead_tc_list.txt can be created by following command:
grep ",dead," synthesized_info.csv | cut -d"," -f1 | sort | uniq > dead_tc_list.txt
"""
import sys
import os
import subprocess
import csv

f = open("dead_tc_list.txt", "r")
tc_name = f.readline()
tc_name = tc_name.replace("\r", "")
tc_name = tc_name.replace("\n", "")
while tc_name:
    result = subprocess.check_output('grep "' + tc_name + '" bug_info_detail.csv | cut -d"," -f3', shell=True)
    result = result.replace("\r", "")
    bug_contained_time_list = result.split("\n")
    bug_contained_time_list.pop()
    if len(bug_contained_time_list) >= 1:
        for bug_contained_time in bug_contained_time_list:
            print bug_contained_time
    tc_name = f.readline()
    tc_name = tc_name.replace("\r", "")
    tc_name = tc_name.replace("\n", "")
