# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

def co_evo_rate_getter(tc_name):
    result = subprocess.check_output('egrep "^' + tc_name + '" co_evolution_rate.csv', shell=True)
    result = result.replace("\r", "")
    result_list = result.split("\n")
    result_list.pop()
    co_evo_list = []
    for x in result_list:
        co_evo_info_list = x.split(",")
        co_evo_list.append(float(co_evo_info_list[-1]))
    return sum(co_evo_list) / float(len(co_evo_list))

def life_time_comit_frequency_status_getter(pjt_name, tc_name):
    result = subprocess.check_output('egrep "^' + tc_name + '" ' + pjt_name + '_tc_lifetime_frequency.csv', shell=True)
    result_list = result.split(",")
    return_list = []
    return_list.append(result_list[1])
    return_list.append(result_list[2])
    return_list.append(result_list[3])
    return return_list

def linked_pc_list_getter(tc_name):
    result = subprocess.check_output('egrep ",' + tc_name + '" pc_tc_link_info.csv', shell=True)
    result_list = result.split("\n")
    return_list = []
    for x in result_list:
        return_list.append(x.split(",")[0])
    return return_list

def linked_pc_num_getter(tc_name):
    result = subprocess.check_output('egrep ",' + tc_name + '" pc_tc_link_info.csv', shell=True)
    result_list = result.split("\n")
    return_list = []
    for x in result_list:
        return_list.append(x.split(",")[0])
    return len(return_list)

def num_bug_getter(linked_pc, tc_born_time, tc_dead_time):
    try:
        result = subprocess.check_output('grep ",' + linked_pc + '" buggy_file_info.csv', shell=True)
        result_list = result.split("\n")
        result_list.pop()
        num_bug = 0
        for x in result_list:
            bug_introducing_time = int(x.split(",")[0])
            if (tc_dead_time >= bug_introducing_time) and (bug_introducing_time >= tc_born_time):
                num_bug += 1
        return num_bug
    except subprocess.CalledProcessError:
        return 0

def ave_bug_calcurator(tc_name, lifetime):
    result = subprocess.check_output('egrep "^' + tc_name + '" ' + pjt_name + '_tc_lifetime_frequency.csv', shell=True)
    result = result.replace("\r", "")
    result = result.replace("\n", "")
    result_list = result.split(",")
    tc_born_time = int(result_list[4])
    tc_dead_time = int(result_list[5])
    linked_pc_list = linked_pc_list_getter(tc_name)
    linked_pc_list.pop()
    num_bug_list = []
    for linked_pc in linked_pc_list:
        num_bug_list.append(num_bug_getter(linked_pc, tc_born_time, tc_dead_time))
    #num_bug_list.remove(0)
    if int(lifetime) == 0:
        num_bug_per_month = float(sum(num_bug_list)) * 30.0 * 1
    else:
        num_bug_per_month = float(sum(num_bug_list)) * ((30.0 * 1) / float(lifetime))
    if len(num_bug_list) == 0:
        return num_bug_per_month
    else:
        return num_bug_per_month / float(len(num_bug_list))


pjt_name = "target"
f = open("importing_tc_list.txt", "r")
line = f.readline()
line = line.replace("\r", "")
line = line.replace("\n", "")
writer = csv.writer(file("synthesized_info.csv", 'w'), lineterminator="\n")
header = ["test code name", "co-evolution rate", "lifetime", "commit frequency", "status", "average bug"]
writer.writerow(header)
linked_pc_counter = []
while line:
    tc_name = line
    try: # checking if the test code has corresponding product code. I mean that linking may not be parfect.
        result = subprocess.check_output('egrep "^' + tc_name + '" co_evolution_rate.csv', shell=True)
    except subprocess.CalledProcessError:
        line = f.readline()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        continue
    co_evo_rate = co_evo_rate_getter(tc_name)
    lt_cf_status_list = life_time_comit_frequency_status_getter(pjt_name, tc_name)
    lifetime = lt_cf_status_list[0]
    frequency = lt_cf_status_list[1]
    status = lt_cf_status_list[2]
    ave_bug = ave_bug_calcurator(tc_name, lifetime)
    info_list = []
    info_list.append(tc_name)
    info_list.append(co_evo_rate)
    info_list.append(lifetime)
    info_list.append(frequency)
    info_list.append(status)
    info_list.append(ave_bug)
    writer.writerow(info_list)
    linked_pc_counter.append(linked_pc_num_getter(tc_name))
    line = f.readline()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
print float(sum(linked_pc_counter)) / float(len(linked_pc_counter))
