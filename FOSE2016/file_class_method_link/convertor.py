# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import csv

read_file_name = 'file_class_method.csv'
f = open(read_file_name, 'r')
write_file_name = read_file_name.replace('.csv', '_converted.csv')
f_write = open(write_file_name, 'w')
writer = csv.writer(f_write, lineterminator='\n', delimiter='|')
line = f.readline()
line = line.replace('\r', '')
line = line.replace('\n', '')
while line:
    line_factor = line.split('|')
    java_name = line_factor[0]
    java_name_path_list = java_name.split('/')
    org_index = java_name_path_list.index('org')
    file_path = '.'.join(java_name_path_list[org_index:-1])
    java_name = '/'.join(java_name_path_list[1:])
    class_name = file_path + '.' + line_factor[1]
    method_name = class_name + '.' + line_factor[2] + '(' + line_factor[3] + ')'
    begin_line = line_factor[4]
    end_line = line_factor[5]
    line_info = [java_name, class_name, method_name, begin_line, end_line]
    writer.writerow(line_info)
    line = f.readline()
    line = line.replace('\r', '')
    line = line.replace('\n', '')
f.close()
f_write.close()
