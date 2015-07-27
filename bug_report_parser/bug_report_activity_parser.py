
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies when the bug is fixed, i.e., when the state of the bug
becomes "RESOLVED", "VERIFIED", or "CLOSED".
At first, this script extracts info. about transitions of the state of the bug.
This is done by parsing the history of the bug.
After that, this script identifies when the bug is fixed.

input: A file that records bug history (not bug report). It is obtained by using Masaki's script.
output: bug ID and the date that the bug is fixed.
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

    # check if the activity exists
    try:
        presence = tree.xpath('//*[@id="bugzilla-body"]/p[2]/text()')
        if presence[0] == "\n    No changes have been made to this bug yet.\n  ":
            match = re.findall(r'[0-9]+', file_name)
            bug_id = match[0]
            return_list = []
            return_list.append(bug_id)
            return_list.append("-1")
            return return_list
    except IndexError:
        presence = tree.xpath('//*[@id="error_msg"]/text()[1]')
        if "You are not authorized to access bug" in presence:
            match = re.findall(r'[0-9]+', file_name)
            bug_id = match[0]
            return_list = []
            return_list.append(bug_id)
            return_list.append("-1")
            return return_list

    tr_len = len(tree.xpath('//*[@id="bugzilla-body"]/table/tr'))
    if tr_len == 0:
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
                fixed_date = fixed_date.replace("-", "/")
                r = re.compile("\d{2}:\d{2}")
                fixed_time = r.findall(activity_detail["when"])[0]
                fixed_date = fixed_date + " " + fixed_time
    match = re.findall(r'[0-9]+', file_name)
    bug_id = match[0]
    return_list = []
    return_list.append(bug_id)
    if fixed_date == "":
        return_list.append("-1")
    else:
        return_list.append(fixed_date)
    return return_list
