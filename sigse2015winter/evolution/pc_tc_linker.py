# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

def tc_identifier(result):
    result = result.replace("\r", "")
    tmp_list = result.split("\n")
    tmp_list.pop()
    tc_list = []
    for tmp in tmp_list:
        tc_list.append(tmp.split(",")[-3])
    tc_list = list(set(tc_list))
    return tc_list

f = open("pc_list.txt")
pc = f.readline()
pc = pc.replace("\r", "")
pc = pc.replace("\n", "")
writer = csv.writer(file('pc_tc_link_info.csv', 'w'), lineterminator="\n")
while pc:
    try:
        result = subprocess.check_output('grep "' + pc + '" imported_pc_list.csv', shell=True)
    except subprocess.CalledProcessError:
        pc = f.readline()
        pc = pc.replace("\r", "")
        pc = pc.replace("\n", "")
        continue
    tc_list = tc_identifier(result)
    if len(tc_list) > 0:
        link_info = []
        link_info.append(pc)
        link_info = link_info + tc_list
        writer.writerow(link_info)
    pc = f.readline()
    pc = pc.replace("\r", "")
    pc = pc.replace("\n", "")
f.close()
