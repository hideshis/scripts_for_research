# -*- coding: utf-8 -*-
"""
this script divides change_history_view.csv into following files:
pc_with_tc_with_bug.csv
pc_with_tc_without_bug.csv
pc_without_tc_with_bug.csv
pc_without_tc_without_bug.csv

input: change_history_view.csv
output: pc_with_tc_with_bug.csv
        pc_with_tc_without_bug.csv
        pc_without_tc_with_bug.csv
        pc_without_tc_without_bug.csv
        bug_having_pc_list.csv
"""

import sys
import subprocess
import os

def pc_with_tc_with_bug_and_pc_with_tc_without_bug_maker():
    f_read = open("bug_having_pc_list.csv", "r")
    bug_having_pc = f_read.readline()
    bug_having_pc = bug_having_pc.replace("\n", "")
    while bug_having_pc:
        cmd = 'grep "' + bug_having_pc + '" tc_having_pc_list.csv >> pc_with_tc_with_bug.csv'
        os.system(cmd)
        cmd = 'grep -v "' + bug_having_pc + '" tc_having_pc_list.csv > tmp.csv'
        os.system(cmd)
        cmd = 'mv tmp.csv tc_having_pc_list.csv'
        os.system(cmd)
        bug_having_pc = f_read.readline()
        bug_having_pc = bug_having_pc.replace("\n", "")
    cmd = 'mv tc_having_pc_list.csv pc_with_tc_without_bug.csv'
    os.system(cmd)
    return

def pc_without_tc_with_bug_and_pc_without_tc_without_bug_maker():
    f_read = open("bug_having_pc_list.csv", "r")
    bug_having_pc = f_read.readline()
    bug_having_pc = bug_having_pc.replace("\n", "")
    while bug_having_pc:
        cmd = 'grep "' + bug_having_pc + '" not_tc_having_pc_list.csv >> pc_without_tc_with_bug.csv'
        os.system(cmd)
        cmd = 'grep -v "' + bug_having_pc + '" not_tc_having_pc_list.csv > tmp.csv'
        os.system(cmd)
        cmd = 'mv tmp.csv not_tc_having_pc_list.csv'
        os.system(cmd)
        bug_having_pc = f_read.readline()
        bug_having_pc = bug_having_pc.replace("\n", "")
    cmd = 'mv not_tc_having_pc_list.csv pc_without_tc_without_bug.csv'
    os.system(cmd)
    return

cmd = 'grep ",test," change_history_view.csv | cut -d\',\' -f1,2,3 > tc_having_pc_list.csv'
os.system(cmd)
cmd = 'grep -v ",test," change_history_view.csv | cut -d\',\' -f1,2,3 > not_tc_having_pc_list.csv'
os.system(cmd)
cmd = 'cat tag_info_introduce.csv | cut -d\',\' -f3 | sort | uniq > bug_having_pc_list.csv'
os.system(cmd)
print "pc_with_tc_with_bug_and_pc_with_tc_without_bug_maker start"
pc_with_tc_with_bug_and_pc_with_tc_without_bug_maker()
print "pc_witout_tc_with_bug_and_pc_without_tc_without_bug_maker start"
pc_without_tc_with_bug_and_pc_without_tc_without_bug_maker()
