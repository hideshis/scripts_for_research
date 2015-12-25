# -*- coding: utf-8 -*-
"""
"""
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess

def co_evolution_rate_calculator(file):
    print file
    f = open(file, "r")
    line = f.readline()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    flag = 0
    co_evolution_counter = 0
    evolution_counter = 0
    subtraction = 0
    change_dict = {'production':0, 'test':0}
    while line:
        evolution_counter += 1
        factor = line.split(",")
        date = factor[1]
        if factor[-1] == "test":
            change_dict['test'] += 1
        else:
            change_dict['production'] += 1
        if flag == 0:
            flag = 1
            check_date = date
            line = f.readline()
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            continue
        if check_date != date:
            if (change_dict['production'] > 0) and (change_dict['test'] > 0):
                co_evolution_counter += 1
                subtraction += (change_dict['production'] + change_dict['test'] - 1)
            change_dict = {'production':0, 'test':0}
            check_date = date
        line = f.readline()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
    f.close()
    print co_evolution_counter, evolution_counter, subtraction
    return float(co_evolution_counter) / (evolution_counter - subtraction)

def pc_name_getter(file):
    result = subprocess.check_output('grep ",production" ' + file + ' | cut -d, -f4 | sort | uniq', shell=True)
    pc_name = result.replace("\r", "")
    pc_name = pc_name.replace("\n", "")
    return pc_name

os.chdir('./evolution_info')
files = os.listdir('.')
tc_list = []
for x in files:
    if (not x.endswith(".csv")) or (x == "co_evolution_rate.csv"):
        continue
    tc_list.append(x.split("__")[0])
tc_list = list(set(tc_list))
writer = csv.writer(file('co_evolution_rate.csv', 'w'), lineterminator="\n")
for tc in tc_list:
    result = subprocess.check_output('ls | grep "' + tc + '"', shell=True)
    result = result.replace("\r", "")
    tc_file_list = result.split("\n")
    tc_file_list.pop()
    co_evolution_rate_list = []
    pc_name_list = []
    for tc_file in tc_file_list:
        co_evolution_rate_list.append(co_evolution_rate_calculator(tc_file))
        pc_name_list.append(pc_name_getter(tc_file))
    co_evolution_rate = float(sum(co_evolution_rate_list)) / float(len(co_evolution_rate_list))
    pc_name = "|".join(pc_name_list)
    tc_name = tc.split("__")[0]
    tc_name = tc_name.replace("_java", ".java")
    tc_name = tc_name.replace("_", "/")
    tc_name = tc_name.replace("/src/test.java/", "/src/test/java/")
    info_list = []
    info_list.append(tc_name)
    info_list.append(pc_name)
    info_list.append(co_evolution_rate)
    writer.writerow(info_list)
os.system("mv co_evolution_rate.csv ..")
