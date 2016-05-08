# -*- coding: utf-8 -*-

import datetime
import subprocess
import sys
import os

def time_getter(line, flag):
    if flag == 'creation':
        time = line.split(',')[3]
    elif flag == 'update':
        time = line.split(',')[4]
    else:
        sys.exit('alk;sdjfal;kjljfals;fkldfjjalfds')
    yymmdd = time.split('T')[0]
    hhmmss = time.split('T')[1]
    hhmmss = hhmmss.split('.')[0]
    return yymmdd + ' ' + hhmmss

def bug_category_getter(creation_time, version):
    try:
        result = subprocess.check_output('grep "' + version + '," tag_info2.csv', shell=True)
    except subprocess.CalledProcessError:
        return 'non existing version'
    tagged_time = result.split(',')[-1]
    tagged_time = tagged_time.replace('\r', '')
    tagged_time = tagged_time.replace('\n', '')
    delta = creation_time - datetime.datetime.strptime(tagged_time, '%Y-%m-%d %H:%M:%S')
    if int(delta.total_seconds()) >= 0:
        return 'post-release bug'
    else:
        return 'pre-release bug'

def history_checker(issue_key, resolution):
    try:
        #result = subprocess.check_output('grep "' + issue_key + '," ./scripts_for_research/ehime/jira/bug_history.csv', shell=True)
        result = subprocess.check_output('grep "' + issue_key + '," ./jira/bug_history.csv', shell=True)
    except subprocess.CalledProcessError:
        return resolution
    result = result.replace('\r', '')
    history_list = result.split('\n')
    history_list.pop()
    for history in history_list:
        if history.endswith(' '):
            history = history[:-1]
        if history.split(',')[-1] == 'Fixed':
            return 'Fixed'
    return resolution

query_list = ['Bug ID,Opened,Changed']
os.system('echo ' + ','.join(query_list) + '>>overlooked_bugs_httpclient.csv')
#f = open('./scripts_for_research/ehime/jira/bug_info.csv', 'r')
f = open('./jira/bug_info.csv', 'r')
line = f.readline()
line = line.replace('\r', '')
line = line.replace('\n', '')
null_counter = 0
pre_counter = 0
post_counter = 0
while line:
    issue_key = line.split(',')[0]
    resolution = line.split(',')[2]
    creation_time = datetime.datetime.strptime(time_getter(line, 'creation'), '%Y-%m-%d %H:%M:%S')
    version = line.split(',')[-1]
    if version.endswith(' '):
        version = version[:-1]
    bug_category = bug_category_getter(creation_time, version)
    if bug_category == 'non existing version':
        null_counter += 1
        line = f.readline()
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        continue
    elif bug_category == 'pre-release bug':
        pre_counter += 1
        line = f.readline()
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        continue
    elif bug_category == 'post-release bug':
        post_counter += 1
    if resolution != 'Fixed':
        resolution = history_checker(issue_key, resolution)
    if resolution == 'Fixed':
        creation_time = time_getter(line, 'creation')
        creation_time = creation_time.replace('-', '/')
        creation_time = creation_time[:-3]
        updated_time = time_getter(line, 'update')
        updated_time = updated_time.replace('-', '/')
        updated_time = updated_time[:-3]
        query_list = [issue_key, creation_time, updated_time]
        os.system('echo ' + ','.join(query_list) + '>>overlooked_bugs_httpclient.csv')
    line = f.readline()
    line = line.replace('\r', '')
    line = line.replace('\n', '')
print null_counter, pre_counter, post_counter
