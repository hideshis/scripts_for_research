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
    cmd = "cat bug_having_pc_list.txt tc_having_pc_list.txt | sort | uniq -d"
    result = subprocess.check_output(cmd, shell=True)
    pc_with_tc_with_bug_list = result.split("\n")
    print "pc_with_tc_with_bug: " + str(len(pc_with_tc_with_bug_list))
    for pc_with_tc_with_bug in pc_with_tc_with_bug_list:
        cmd = 'grep ",' + pc_with_tc_with_bug + '," change_history_view.csv >> pc_with_tc_with_bug.csv'
        os.system(cmd)
        cmd = 'grep ",' + pc_with_tc_with_bug + '," tag_info_introduce.csv >> pc_with_tc_with_bug.csv'
        os.system(cmd)
    cmd = "cat not_bug_having_pc_list.txt tc_having_pc_list.txt | sort | uniq -d"
    result = subprocess.check_output(cmd, shell=True)
    pc_with_tc_without_bug_list = result.split("\n")
    print "pc_with_tc_without_bug: " + str(len(pc_with_tc_without_bug_list))
    for pc_with_tc_without_bug in pc_with_tc_without_bug_list:
        cmd = 'grep ",' + pc_with_tc_without_bug + '," change_history_view.csv >> pc_with_tc_without_bug.csv'
        os.system(cmd)
        cmd = 'grep ",' + pc_with_tc_without_bug + '," tag_info_introduce.csv >> pc_with_tc_without_bug.csv'
        os.system(cmd)
    return

def pc_without_tc_with_bug_and_pc_without_tc_without_bug_maker():
    cmd = "cat bug_having_pc_list.txt not_tc_having_pc_list.txt | sort | uniq -d"
    result = subprocess.check_output(cmd, shell=True)
    pc_without_tc_with_bug_list = result.split("\n")
    print "pc_without_tc_with_bug: " + str(len(pc_without_tc_with_bug_list))
    for pc_without_tc_with_bug in pc_without_tc_with_bug_list:
        cmd = 'grep ",' + pc_without_tc_with_bug + '," change_history_view.csv >> pc_without_tc_with_bug.csv'
        os.system(cmd)
        cmd = 'grep ",' + pc_without_tc_with_bug + '," tag_info_introduce.csv >> pc_without_tc_with_bug.csv'
        os.system(cmd)
    cmd = "cat not_bug_having_pc_list.txt not_tc_having_pc_list.txt | sort | uniq -d"
    result = subprocess.check_output(cmd, shell=True)
    pc_without_tc_without_bug_list = result.split("\n")
    print "pc_without_tc_without_bug: " + str(len(pc_without_tc_without_bug_list))
    for pc_without_tc_without_bug in pc_without_tc_without_bug_list:
        if pc_without_tc_without_bug == "File\r":
            continue
        cmd = 'grep ",' + pc_without_tc_without_bug + '," change_history_view.csv >> pc_without_tc_without_bug.csv'
        os.system(cmd)
        cmd = 'grep ",' + pc_without_tc_without_bug + '," tag_info_introduce.csv >> pc_without_tc_without_bug.csv'
        os.system(cmd)
    return

def not_tc_having_pc_list_maker():
    cmd = 'cp pc_list.txt not_tc_having_pc_list.txt'
    os.system(cmd)
    f = open("tc_having_pc_list.txt", "r")
    tc_having_pc = f.readline()
    tc_having_pc = tc_having_pc.replace("\n", "")
    while tc_having_pc:
        cmd = 'grep -v "' + tc_having_pc + '" not_tc_having_pc_list.txt > tmp.txt'
        os.system(cmd)
        cmd = 'mv tmp.txt not_tc_having_pc_list.txt'
        os.system(cmd)
        tc_having_pc = f.readline()
        tc_having_pc = tc_having_pc.replace("\n", "")
    f.close()
    cmd = 'sed -e "s/\\n/\\r\\n/g" not_tc_having_pc_list.txt > tmp.txt'
    os.system(cmd)
    cmd = 'mv tmp.txt not_tc_having_pc_list.txt'
    os.system(cmd)
    return

def not_bug_having_pc_list_maker():
    cmd = 'cp pc_list.txt not_bug_having_pc_list.txt'
    os.system(cmd)
    f = open("bug_having_pc_list.txt", "r")
    bug_having_pc = f.readline()
    bug_having_pc = bug_having_pc.replace("\n", "")
    while bug_having_pc:
        cmd = 'grep -v "' + bug_having_pc + '" not_bug_having_pc_list.txt > tmp.txt'
        os.system(cmd)
        cmd = 'mv tmp.txt not_bug_having_pc_list.txt'
        os.system(cmd)
        bug_having_pc = f.readline()
        bug_having_pc = bug_having_pc.replace("\n", "")
    f.close()
    cmd = 'sed -e "s/\\n/\\r\\n/g" not_bug_having_pc_list.txt > tmp.txt'
    os.system(cmd)
    cmd = 'mv tmp.txt not_bug_having_pc_list.txt'
    os.system(cmd)
    return


#cmd = 'grep ",test," change_history_view.csv | cut -d\',\' -f1,2,3,4 > tc_having_pc_list.csv'
cmd = 'grep ",test," change_history_view.csv | cut -d\',\' -f3 | sort | uniq > tc_having_pc_list.txt'
os.system(cmd)
cmd = 'cat change_history_view.csv | cut -d\',\' -f3 | sort | uniq > pc_list.txt'
os.system(cmd)
not_tc_having_pc_list_maker()
#cmd = 'grep -v ",test," change_history_view.csv | cut -d\',\' -f1,2,3,4 > not_tc_having_pc_list.csv'
#os.system(cmd)
cmd = 'cat tag_info_introduce.csv | cut -d\',\' -f3 | sort | uniq > bug_having_pc_list.txt'
os.system(cmd)
not_bug_having_pc_list_maker()
print "pc_with_tc_with_bug_and_pc_with_tc_without_bug_maker start"
pc_with_tc_with_bug_and_pc_with_tc_without_bug_maker()
print "pc_witout_tc_with_bug_and_pc_without_tc_without_bug_maker start"
pc_without_tc_with_bug_and_pc_without_tc_without_bug_maker()
