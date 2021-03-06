# -*- coding: utf-8 -*-
"""
This script collects JIRA's issue reports.
It also collects the history of changes of resolution.
"""

import jira
from jira.client import JIRA
from jira.exceptions import JIRAError
import json
import sys
import os
import time
import csv

def removeCRLF(target):
    target = target.replace('\r', '')
    target = target.replace('\n', '')
    return target

f_info = open('bug_info.csv', 'w')
writer_info = csv.writer(f_info, lineterminator='\n')
f_history = open('bug_history.csv', 'w')
writer_history = csv.writer(f_history, lineterminator='\n')
options = {'server': 'https://issues.apache.org/jira',}
jira = JIRA(options, basic_auth=(user_name, pass_word))
projects = jira.projects()
for jira_id in range(782, 1732):
    key = 'HTTPCLIENT-' + str(jira_id)
    print key + ' is now on processing.'
    try:
        issue = jira.issue(key)
    except JIRAError as e:
        if e.status_code == 404:
            print "issue does not exist."
            continue
    issue_type = removeCRLF(issue.fields.issuetype.name)
    if issue.fields.resolution is None:
        resolution = 'null'
    else:
        resolution = removeCRLF(issue.fields.resolution.name)
    created = removeCRLF(issue.fields.created)
    if issue.fields.updated is None:
        updated = 'null'
    else:
        updated = removeCRLF(issue.fields.updated)
    if issue.fields.resolutiondate is None:
        resolved = 'null'
    else:
        resolved = removeCRLF(issue.fields.resolutiondate)
    #if issue.fields.versions is None:
    if len(issue.fields.versions) == 0:
        version = 'null'
    else:
        version = removeCRLF(str(issue.fields.versions[0]))
    if issue_type == 'Bug':
        # CSV に書き込み
        """
        query = issue.key + ','  + issue_type + ',' + resolution + ',' + created + ',' + updated + ',' + resolved + ',' + version
        os.system('echo ' + query + '>> bug_info.csv')
        """
        query = [issue.key, issue_type, resolution, created, updated, resolved, version]
        writer_info.writerow(query)
        # resolution の状態遷移取得
        issue = jira.issue(key, expand='changelog')
        #print json.dumps(issue.raw)
        changelog = issue.changelog
        for history in changelog.histories:
            for item in history.items:
                if item.field == 'resolution':
                    if item.fromString is None:
                        item.fromString = 'null'
                    if item.toString is None:
                        item.toString = 'null'
                    """
                    query = issue.key + ',' + history.created + ',' + item.fromString + ',' + item.toString
                    os.system('echo ' + query + '>> bug_history.csv')
                    """
                    query = [issue.key,history.created,item.fromString,item.toString]
                    writer_history.writerow(query)
    time.sleep(3.0)
f_info.close()
f_history.close()
