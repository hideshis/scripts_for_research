# -*- coding: utf-8 -*-
"""
This script formats the contents of tag_info.csv in order to make it easer to use.
tag_info.csv can be obtained by the following command:
git log --tags --simplify-by-decoration --pretty="format:%ai,%d" > tag_info.csv
"""
import datetime
import os

def tagged_time_getter(line):
    tagged_time = line.split(',')[0]
    tagged_time = tagged_time[:-6]
    return tagged_time

def tag_name_getter(line):
    tag_name = line.split(',')[-1]
    tag_name = tag_name[7:-1]
    return tag_name

f = open('tag_info.csv', 'r')
f_write = open('tag_info2.csv', 'w')
writer = csv.writer(f_write, lineterminator='\n')
line = f.readline()
line = line.replace('\r', '')
line = line.replace('\n', '')
while line:
    if not ', (tag: ' in line:
        line = f.readline()
        line = line.replace('\r', '')
        line = line.replace('\n', '')
        continue
    tagged_time = tagged_time_getter(line)
    tag_name = tag_name_getter(line)
    query_list = [tag_name, tagged_time]
    #os.system('echo ' + ','.join(query_list) + '>>tag_info2.csv')
    writer = csv.writerow(query_list)
    line = f.readline()
    line = line.replace('\r', '')
    line = line.replace('\n', '')
f.close()
f_write.close()
