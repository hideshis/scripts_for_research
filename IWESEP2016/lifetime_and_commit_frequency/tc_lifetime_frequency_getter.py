# -*- coding: utf-8 -*-
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess
import numpy
import time

def commit_time_list_getter(tc):
    result = subprocess.check_output('grep ",' + tc + '" target_all.csv | cut -d"," -f2', shell=True)
    result = result.replace('\r', '')
    result_list = result.split()
    commit_time_list = []
    for result in result_list:
        commit_time_list.append(int(result))
    commit_time_list.sort()
    return commit_time_list

def dead_arrive_checker(tc):
    os.chdir('./target')
    dead_or_arrive = subprocess.check_output('git log --name-status -n 1 -- ' + tc, shell=True)
    os.chdir('..')
    dead_or_arrive = dead_or_arrive.replace('\r', '')
    doa_list = dead_or_arrive.split("\n")
    if doa_list[-2].startswith("D"): # the file have been deleted
        return "dead"
    else: # the file have been arrive now
        return "arrive"

def lifetime_getter(born_time_unix, dead_time_unix):
    born_time = datetime.datetime.fromtimestamp(born_time_unix)
    dead_time = datetime.datetime.fromtimestamp(dead_time_unix)
    lifetime = (dead_time - born_time).days
    return lifetime

pjt_name = "target"
allLines = open('tc_list.txt').read()
allLines = allLines.replace('\r', '')
tc_list = allLines.split('\n')
tc_list.pop()
writer = csv.writer(file(pjt_name + "_tc_lifetime_frequency.csv", 'w'))
header = ["tc_name", "lifetime", "commit frequency", "status", "born", "dead"]
writer.writerow(header)
for tc in tc_list:
    commit_time_list = commit_time_list_getter(tc)
    status = dead_arrive_checker(tc)
    born_time_unix = commit_time_list[0]
    if status == "arrive":
        dead_time_unix = int(time.time())
    elif status == "dead":
        dead_time_unix = commit_time_list[-1]
    else:
        sys.exit('error in doa')
    lifetime = lifetime_getter(born_time_unix, dead_time_unix)
    commit_frequency = len(commit_time_list)
    info_list = []
    info_list.append(tc) # tc's name
    info_list.append(lifetime) # lifetime
    info_list.append(commit_frequency) # commit frequency
    info_list.append(status)
    info_list.append(born_time_unix)
    info_list.append(dead_time_unix)
    writer.writerow(info_list)
