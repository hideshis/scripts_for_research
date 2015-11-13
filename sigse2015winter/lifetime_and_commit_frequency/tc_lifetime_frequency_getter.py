# -*- coding: utf-8 -*-
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess
import numpy

"""
# average
def commit_frequency_getter(tc, num_of_times_of_commit, commit_date_list):
    flag = 0
    lifetime_sum = 0
    for commit_date in commit_date_list:
        if flag == 0:
            initial_date = datetime.datetime.fromtimestamp(int(commit_date))
            flag = 1
            continue
        final_date = datetime.datetime.fromtimestamp(int(commit_date))
        lifetime = (final_date - initial_date).days
        lifetime_sum += lifetime
        initial_date = final_date
    return lifetime_sum / (num_of_times_of_commit - 1)
"""

# median
def commit_frequency_getter(tc, num_of_times_of_commit, commit_date_list):
    flag = 0
    lifetime_list = []
    for commit_date in commit_date_list:
        if flag == 0:
            initial_date = datetime.datetime.fromtimestamp(int(commit_date))
            flag = 1
            continue
        final_date = datetime.datetime.fromtimestamp(int(commit_date))
        lifetime = (final_date - initial_date).days
        lifetime_list.append(lifetime)
        initial_date = final_date
    return numpy.median(lifetime_list)



def lifetime_frequency_getter(tc, pjt_name):
    os.chdir("./" + pjt_name)

    result = subprocess.check_output('git log --pretty=format:"%at" --reverse -- ' + tc, shell=True)
    result = result.replace('\r', '')
    initial_date_unix = result.split('\n')[0]
    initial_date = datetime.datetime.fromtimestamp(int(initial_date_unix))

    dead_or_arrive = subprocess.check_output('git log --name-status -n 1 -- ' + tc, shell=True)
    dead_or_arrive = dead_or_arrive.replace('\r', '')
    doa_list = dead_or_arrive.split("\n")
    print doa_list[-2]
    if doa_list[-2].startswith("D"): # the file have been deleted
        final_date_unix = subprocess.check_output('git log --pretty=format:"%at" -n 1 -- ' + tc, shell=True)
        final_date_unix = final_date_unix.replace("\r", "")
        final_date_unix = final_date_unix.replace("\n", "")
        final_date = datetime.datetime.fromtimestamp(int(final_date_unix))
        flag = "dead"
    else: # the file have been arrive now
        final_date_unix = subprocess.check_output('git log --pretty=format:"%at" -n 1', shell=True)
        final_date_unix = final_date_unix.replace("\r", "")
        final_date_unix = final_date_unix.replace("\n", "")
        final_date = datetime.datetime.fromtimestamp(int(final_date_unix))
        flag = "arrive"
    print initial_date, final_date
    lifetime = (final_date - initial_date).days
    print lifetime

    commit_dates = subprocess.check_output('git log --pretty=format:"%at" --reverse -- ' + tc, shell=True)
    commit_dates = commit_dates.replace("\r", "")
    commit_date_list = commit_dates.split("\n")
    if flag == "arrive":
        commit_date_list.append(final_date_unix)
    num_of_times_of_commit = len(commit_date_list)
    print commit_date_list
    print num_of_times_of_commit
    commit_frequency = commit_frequency_getter(tc, num_of_times_of_commit, commit_date_list)
    print commit_frequency
    os.chdir("..")
    return_list = []
    return_list.append(lifetime)
    return_list.append(commit_frequency)
    return return_list

argvs = sys.argv
pjt_name = argvs[1]
f = open(pjt_name + "_tc.csv", "r")
line = f.readline()
tc_list = []
# get the test code's list
while line:
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    tc_list_in_a_commit = line.split(",")
    del tc_list_in_a_commit[0] # remove commit hash
    tc_list = tc_list + tc_list_in_a_commit
    tc_list = list(set(tc_list))
    line = f.readline()
f.close()

writer = csv.writer(file(pjt_name + "_tc_lifetime_frequency.csv", 'w'))
header = ["tc_name", "lifetime", "commit frequency"]
writer.writerow(header)
for tc in tc_list:
    info_list = []
    info_list.append(tc) # tc's name
    result = lifetime_frequency_getter(tc, pjt_name)
    info_list.append(result[0]) # lifetime
    info_list.append(result[1]) # commit frequency
    writer.writerow(info_list)
