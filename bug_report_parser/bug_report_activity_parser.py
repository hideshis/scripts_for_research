
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies when the bug is fixed, i.e., when the state of the bug
becomes "RESOLVED", "VERIFIED", or "CLOSED".
At first, this script extracts info. about transitions of the state of the bug.
This is done by parsing the history of the bug.
After that, this script identifies when the bug is fixed.

input: A file that records bug history (not bug report). It is obtained by using Masaki's script.
output: the date that the bug is fixed.
"""
import os
import sys
import commands
import subprocess
import re
from lxml import html

def str_format(src):
    src = src.replace("\n", "")
    src = src.replace(" ", "")
    return src

def extraction(file_name):
    html_string = open(file_name).read()
    tree = html.fromstring(html_string)
    tr_len = len(tree.xpath('//*[@id="bugzilla-body"]/table/tr'))
    if tr_len == 0:
        print "null activity"
        return
    fixed_date = ""
    for tr_num in range(2, tr_len+1):
        activity_detail = {"who":"", "when":"", "what":"", "removed":"", "added":""}
        xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td'
        td_len = len(tree.xpath(xpath))
        if td_len == 3:
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[1]/text()'
            activity_detail["what"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[2]/text()'
            activity_detail["removed"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[3]/text()'
            activity_detail["added"] = str_format(tree.xpath(xpath)[0])
            activity_detail["when"] = when
        if td_len == 5:
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[1]/text()'
            activity_detail["who"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[2]/text()'
            activity_detail["when"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[3]/text()'
            activity_detail["what"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[4]/text()'
            activity_detail["removed"] = str_format(tree.xpath(xpath)[0])
            xpath = '//*[@id="bugzilla-body"]/table/tr' + '[' + str(tr_num) + ']' + '/td[5]/text()'
            activity_detail["added"] = str_format(tree.xpath(xpath)[0])
            when = activity_detail["when"]
        if (activity_detail["what"] == "Status"):
            if (activity_detail["added"] == "REOPENED"):
                fixed_date = ""
            elif (activity_detail["added"] == "RESOLVED") or (activity_detail["added"] == "VERIFIED") or (activity_detail["added"] == "CLOSED"):
                r = re.compile("\d{4}-\d{2}-\d{2}")
                fixed_date = r.findall(activity_detail["when"])[0]
    if fixed_date == "":
        print "this bug is not fixed"
    else:
        print "fixed date: " + fixed_date
    return

    """
    # extract info. about transitions of the state of the bug
    # the deliverable is bug_report_activity_sample_dripped.hoge
    # bug_report_activity_sample_dripped.hoge contains only the history of status changes
    command = "grep -n \"table\" " + file_name + " > bug_report_history_tmp1.txt"
    os.system(command)
    command = "grep -n \"table border cellpadding=\\\"4\\\"\" bug_report_history_tmp1.txt | cut -d : -f1 > bug_report_history_tmp2.txt"
    os.system(command)
    command = "cat bug_report_history_tmp2.txt"
    checker = subprocess.check_output(command)
    if checker == "":
        command = "rm bug_report_history_tmp*.txt"
        os.system(command)
        print "no history"
        return
    start_point_meta = int(subprocess.check_output(command))
    checker = ""
    end_point_meta = start_point_meta
    while not "</table>" in checker:
        end_point_meta = end_point_meta + 1
        command = "sed -n '" + str(end_point_meta) + "," + str(end_point_meta) + "p' bug_report_history_tmp1.txt"
        checker = subprocess.check_output(command)
    #print start_point_meta, end_point_meta
    command = "sed -n '" + str(start_point_meta) + "," + str(start_point_meta) + "p' bug_report_history_tmp1.txt | cut -d : -f1"
    start_point = subprocess.check_output(command, shell=True)
    start_point = start_point.replace("\n", "")
    command = "sed -n '" + str(end_point_meta) + "," + str(end_point_meta) + "p' bug_report_history_tmp1.txt | cut -d : -f1"
    end_point = subprocess.check_output(command, shell=True)
    end_point = end_point.replace("\n", "")
    #print start_point, end_point
    command = "sed -n '" + start_point + "," + end_point + "p' " + file_name + " > bug_report_activity_sample_dripped.hoge"
    os.system(command)

    # identify when the bug is fixed
    command = "sed -e \"s/<tr>/<tr>\\n/g\" bug_report_activity_sample_dripped.hoge > hogehoge.hoge"
    os.system(command)
    command = "sed -e \"s/<\\/tr>/<\\/tr>\\n/g\" hogehoge.hoge > hogehoge2.hoge"
    os.system(command)
    command = "rm hogehoge.hoge"
    os.system(command)
    command = "mv hogehoge2.hoge bug_report_activity_sample_dripped.hoge"
    os.system(command)
    command = "egrep -n \"<tr>|</tr>\" bug_report_activity_sample_dripped.hoge | cut -d : -f1 > bug_report_table_info.hoge"
    os.system(command)
    command = "wc -l bug_report_table_info.hoge"
    routine_times = (subprocess.check_output(command)).split(' ')[-2]
    #print routine_times
    routine_times = int(routine_times) / 2
    line_number = 3
    fixed_date = ""
    for x in range(0, routine_times):
        command = "sed -n '"+ str(line_number) + "," + str(line_number) + "p' bug_report_table_info.hoge"
        start_point = subprocess.check_output(command)
        start_point = start_point.replace("\n", "")
        line_number = line_number + 1
        command = "sed -n '"+ str(line_number) + "," + str(line_number) + "p' bug_report_table_info.hoge"
        end_point = subprocess.check_output(command)
        end_point = end_point.replace("\n", "")
        #print start_point, end_point
        command = "sed -n '" + start_point + "," + end_point + "p' bug_report_activity_sample_dripped.hoge"
        tr_group = subprocess.check_output(command)
        tr_group = tr_group.replace("\n", "")
        tr_group = tr_group.replace(" ", "")
        flag = 0
        super_flag = 0
        tr_line_number = line_number + 1
        if tr_line_number > (routine_times * 2):
            flag = 1
        while flag == 0:
            command = "sed -n '"+ str(tr_line_number) + "," + str(tr_line_number) + "p' bug_report_table_info.hoge"
            tr_start_point = subprocess.check_output(command)
            tr_start_point = tr_start_point.replace("\n", "")
            tr_line_number = tr_line_number + 1
            command = "sed -n '"+ str(tr_line_number) + "," + str(tr_line_number) + "p' bug_report_table_info.hoge"
            tr_end_point = subprocess.check_output(command)
            tr_end_point = tr_end_point.replace("\n", "")
            command = "sed -n '" + tr_start_point + "," + tr_end_point + "p' bug_report_activity_sample_dripped.hoge"
            tr = subprocess.check_output(command)
            tr = tr.replace("\n", "")
            tr = tr.replace(" ", "")
            r = re.compile("\d{4}-\d{2}-\d{2}")
            match = r.findall(tr)
            if len(match) == 0:
                tr_group = tr_group + tr
                line_number = tr_line_number
            elif len(match) == 1:
                flag = 1
            else:
                print match
                #sys.exit(match)
            tr_line_number = tr_line_number + 1
            if tr_line_number > (routine_times * 2):
                break
        key_words = ["<td>RESOLVED</td>", "<td>VERIFIED</td>", "<td>CLOSED</td>"]
        # if the status is one of the key_words, then output the date
        if ("Status" in tr_group) and ((key_words[0] in tr_group) or (key_words[1] in tr_group) or (key_words[2] in tr_group)):
            r = re.compile("\d{4}-\d{2}-\d{2}")
            fixed_date = r.findall(tr_group)
            # when the bug is repoened, the bug cannot be recognized as fixed
            condition1 = "<td>Status</td>" + key_words[0] + "<td>REOPENED</td>"
            condition2 = "<td>Status</td>" + key_words[1] + "<td>REOPENED</td>"
            condition3 = "<td>Status</td>" + key_words[2] + "<td>REOPENED</td>"
            if (condition1 in tr_group) or (condition2 in tr_group) or (condition3 in tr_group):
                fixed_date = ""
        line_number = line_number + 1
        if line_number > (routine_times * 2):
            break
    if fixed_date == "":
        print "this bug is not fixed"
    else:
        print "fixed_date: " + fixed_date[0]
    """
    if file_name == "activity290005.cgi":
        sys.exit("execution abortion")
    """
    return
    """
