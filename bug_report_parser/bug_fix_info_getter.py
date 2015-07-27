#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies following info.
from the bug report:
    1. bug ID
    2. Craetion date of the report
    3. last modified date of the bug report
    4. the latest status of the bug
from the bug fixing history:
    1. the date of the bug fixing

input: Bug reports obtained by using Masaki's script.
output: above info.
assumed directory structure:
./__bug_fix_info_getter.py
  |_(project name)/__activity_(num)_(num)/activity_(num).cgi
                   |_bug_(num)_(num)/issue(num).cgi
"""
import bug_report_activity_parser
import bug_report_parser

import os
import sys
import commands
import subprocess
import re
import csv

def join(bug_id):
    writer = csv.writer(file("eclipse"+bug_id+".csv", 'w'), lineterminator="\n")
    header = ["Bug ID", "Opened", "Changed"]
    writer.writerow(header)
    for line_num in range(1, 10001):
        row = []
        cmd = "sed -n '" + str(line_num) +"p' result_report.csv" # extract nth line from result_report.csv
        output = subprocess.check_output(cmd)
        row.append(output.split(",")[0]) # bug ID
        row.append(output.split(",")[1].replace("\n", "")) # Created date
        if output.split(",")[1].replace("\n", "") == "-1": # if Created date is -1
            continue
        cmd = "sed -n '" + str(line_num) +"p' result_activity.csv" # extract nth line from result_report.csv
        output = subprocess.check_output(cmd)
        row.append(output.split(",")[1].replace("\n", "")) # last changed date
        if output.split(",")[1].replace("\n", "") == "-1": # if last changed date is -1
            continue
        writer.writerow(row)
    return

def bug_info_extraction(bug_id, bug_id_start, bug_id_end):
    # dive into activity_(bug_id) direcetory
    print "start activity"
    os.chdir("./activity" + bug_id)
    list_file = os.listdir(".")
    for file_name in list_file:
        if not file_name.startswith("activity"):
            continue
        #print file_name
        result_list = bug_report_activity_parser.extraction(file_name)
        text = result_list[0] + "," + result_list[1]
        os.system("echo " + text + ">>result_activity.csv")
    os.system("rm bug_report_history_tmp*.txt")
    os.system("rm bug_report_table_info.hoge")
    os.system("rm bug_report_activity_sample_dripped.hoge")
    os.system("egrep -v '^\s*$' result_activity.csv > tmp.csv") # remove brank lines
    os.system("mv tmp.csv result_activity.csv")
    os.system("sort -t ',' -k 1n,1 result_activity.csv > tmp.csv")
    os.system("mv tmp.csv result_activity.csv")
    os.system("mv result_activity.csv ..")
    os.chdir("..")

    # dive into bug_(bug_id) direcetory
    print "start report"
    os.chdir("bug" + bug_id)
    list_file = os.listdir(".")
    for file_name in list_file:
        if not file_name.startswith("issue"):
            continue
        #print file_name
        result_list = bug_report_parser.extraction(file_name)
        text = result_list[0] + "," + result_list[1]
        os.system("echo " + text + ">>result_report.csv")
    os.system("egrep -v '^\s*$' result_report.csv > tmp.csv") # remove brank lines
    os.system("mv tmp.csv result_report.csv")
    os.system("sort -t ',' -k 1n,1 result_report.csv > tmp.csv")
    os.system("mv tmp.csv result_report.csv")
    os.system("mv result_report.csv ..")
    os.chdir("..")

    print "start join"
    join(bug_id)
    os.system("rm result_activity.csv")
    os.system("rm result_report.csv")

if __name__ == '__main__':
    print "project name: "
    pjt_name = raw_input()

    # dive into the (project name) directory
    os.chdir("./" + pjt_name)

    # get the directory names of current directory
    list_directory = os.listdir(".")
    bug_id_list = []
    for directory in list_directory:
        # extract "_(num)_(num)" from the directory name
        if directory.startswith("activity"):
            bug_id_info = directory.replace("activity", "")
            bug_id_list.append(bug_id_info)

    # extract needed info. from bug reports
    for bug_id in bug_id_list:
        print bug_id
        r = re.compile("[0-9]+")
        match = r.findall(bug_id)
        bug_id_start = int(match[0]) * 10000
        bug_id_end = int(match[1]) * 10000
        print "bugs with ID from " + str(bug_id_start) + " to " + str(bug_id_end) + " are parsed from now"
        bug_info_extraction(bug_id, bug_id_start, bug_id_end)
