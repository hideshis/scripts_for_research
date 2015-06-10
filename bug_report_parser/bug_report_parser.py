#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies following info.:
1. bug ID
2. Craetion date of the report
3. last modified date of the bug report
4. the latest status of the bug

input: Bug report. It is obtained by using Masaki's script.
output: Info. cited above.
"""
import os
import sys
import commands
import subprocess
import re
from lxml import html

def extraction(file_name):
    html_string = open(file_name).read()
    tree = html.fromstring(html_string)

    # extracting bug ID
    bug_id_html = tree.xpath('//*[@id="changeform"]/div[1]/a/b/text()')
    r = re.compile("[0-9]+")
    try:
        match = r.search(bug_id_html[0])
    except IndexError:
        print "this bug report does not exist"
        return
    bug_id = match.group(0)
    print "Bug ID:                                     " + bug_id
    """
    command = "grep \"<b>Bug&nbsp;\" " + file_name
    try:
        bug_id_containing_line = subprocess.check_output(command)
    except subprocess.CalledProcessError:
        print "no bug report here"
        return
    r = re.compile("Bug&nbsp;[0-9]+")
    match = r.search(bug_id_containing_line)
    bug_id = match.group(0).split(";")[1]
    print "Bug ID:                                     " + bug_id
    """

    # extracting creation date of the report
    creation_date_html = tree.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[1]/td/text()')
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    match = r.search(creation_date_html[0])
    creation_date = match.group(0)
    print "Creation date: " + creation_date
    """
    #command = "grep -n \"<b>Reported</b>:\" " + file_name
    command = "grep -n \"<th class=\"field_label\">\n      Reported\n    </th>:\" " + file_name
    creation_date_containing_line = subprocess.check_output(command)
    start_from = int(creation_date_containing_line.split(":")[0])
    to_end = start_from + 10
    command = "sed -n \"" + str(start_from) + "," + str(to_end) + "p\" " + file_name
    creation_date_containing_line = subprocess.check_output(command)
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    match = r.search(creation_date_containing_line)
    creation_date = match.group(0)
    print "Creation date: " + creation_date
    """

    # extracting the last modified date of the bug report
    modified_date_html = tree.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[2]/td/text()[1]')
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    match = r.search(modified_date_html[0])
    modified_date = match.group(0)
    print "Modified date: " + modified_date
    """
    #command = "grep -n \"<b> Modified</b>\" " + file_name
    command = "egrep -n \"^      Modified:$\" " + file_name
    modified_date_containing_line = subprocess.check_output(command)
    start_from = int(modified_date_containing_line.split(":")[0])
    to_end = start_from + 10
    command = "sed -n \"" + str(start_from) + "," + str(to_end) + "p\" " + file_name
    modified_date_containing_line = subprocess.check_output(command)
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    match = r.search(modified_date_containing_line)
    modified_date = match.group(0)
    print "Modified date: " + modified_date
    """

    # extracting the latest status of the bug
    latest_status_html = tree.xpath('//*[@id="static_bug_status"]/text()')
    latest_status = latest_status_html[0]
    latest_status = latest_status.replace("\n", "")
    latest_status = re.sub(r' +', ' ', latest_status)
    if latest_status == "CLOSED DUPLICATE of ":
        latest_status = "CLOSED DUPLICATE"
    if latest_status == "RESOLVED DUPLICATE of ":
        latest_status = "RESOLVED DUPLICATE"
    #r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    #match = r.search(modified_date_html[0])
    #modified_date = match.group(0)
    #print "Modified date: " + modified_date
    print "Latest state: " + latest_status
    return
    """
    command = "grep -n \"static_bug_status\" " + file_name
    latest_state_containing_line = subprocess.check_output(command)
    start_from = int(latest_state_containing_line.split(":")[0])
    to_end = start_from + 5
    command = "sed -n \"" + str(start_from) + "," + str(to_end) + "p\" " + file_name
    latest_state_containing_line = subprocess.check_output(command)
    latest_state_containing_line = latest_state_containing_line.replace("\n", "")
    latest_state_containing_line = re.sub(r' +', " ", latest_state_containing_line)
    split_str = "<span id=\"static_bug_status\">"
    latest_state = latest_state_containing_line.split(split_str)[1]
    split_str = "</span>"
    latest_state = latest_state.split(split_str)[0]
    if latest_state[-1] == " ":
        latest_state = latest_state[:-1]
    if latest_state.startswith("CLOSED DUPLICATE"):
        latest_state = "CLOSED DUPLICATE"
    elif latest_state.startswith("RESOLVED DUPLICATE"):
        latest_state = "RESOLVED DUPLICATE"
    print "Latest state: " + latest_state
    """
