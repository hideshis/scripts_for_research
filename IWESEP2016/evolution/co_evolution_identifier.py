# -*- coding: utf-8 -*-
"""
"""
import re
import sys
import csv
import os.path
import os
import datetime

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

os.chdir('./evolution_info')
files = os.listdir('.')
writer = csv.writer(file('co_evolution_rate.csv', 'w'), lineterminator="\n")
for file in files:
    if not file.endswith("_java.csv"):
        continue
    co_evolution_rate = co_evolution_rate_calculator(file)
    file_name = file.replace("_java.csv", ".java")
    file_name = file_name.replace("_", "/")
    info_list = []
    info_list.append(file_name)
    info_list.append(co_evolution_rate)
    writer.writerow(info_list)
os.system("mv co_evolution_rate.csv ..")
