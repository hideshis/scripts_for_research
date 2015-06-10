
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
# 各ライブラリのインポート
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

if __name__ == "__main__":
    extraction("issue_report_history_sample.html")
