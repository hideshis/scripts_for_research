#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies following info.:
1. bug ID
2. Craetion date of the report
3. last modified date of the bug report

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
        #print "this bug report does not exist"
        match = re.findall(r'[0-9]+', file_name)
        bug_id = match[0]
        return_list = []
        return_list.append(bug_id)
        return_list.append("-1")
        return return_list
    bug_id = match.group(0)
    #print "Bug ID: " + bug_id

    # extracting creation date of the report
    creation_date_html = tree.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[1]/td/text()')
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}")
    match = r.search(creation_date_html[0])
    creation_date = match.group(0)
    creation_date = creation_date.replace("-", "/")
    #print "Creation date: " + creation_date

    """
    # extracting the last modified date of the bug report
    modified_date_html = tree.xpath('//*[@id="bz_show_bug_column_2"]/table/tr[2]/td/text()[1]')
    r = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}")
    match = r.search(modified_date_html[0])
    modified_date = match.group(0)
    print "Modified date: " + modified_date

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
    """
    match = re.findall(r'[0-9]+', file_name)
    bug_id = match[0]
    return_list = []
    return_list.append(bug_id)
    return_list.append(creation_date)
    return return_list
