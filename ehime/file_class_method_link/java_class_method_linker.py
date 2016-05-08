# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import csv
import re

def class_info_getter(f, directory):
    class_dict = {}
    class_dict['name'] = f
    class_dict['path'] = directory
    class_dict['full path'] = class_dict['path'] + '/' + class_dict['name']
    return class_dict

def java_dict_getter(class_dict, info):
    java_dict = {}
    java_dict['name'] = info.split('"')[1]
    java_dict['path'] = class_dict['path'].replace('/target/classes/', '/src/main/java/')
    java_dict['full path'] = java_dict['path'] + '/' + java_dict['name']
    if os.path.exists(java_dict['full path']) is False:
        print '!?!?!?wwww!?wwwwww!?!?!?wwwww!?!?!?!?!?!?!?www'
        sys.exit()
    return java_dict

def javap_exe(class_dict):
    cmd = 'javap -private -l ' + class_dict['full path']
    result = subprocess.check_output(cmd, shell=True)
    result = result.replace('\r', '')
    return result.split('\n')

def class_detail_info_getter(class_dict):
    cmd = 'javap ' + class_dict['full path']
    result = subprocess.check_output(cmd, shell=True)
    result = result.replace('\r', '')
    return result.split('\n')[:-1]

# xxx yyy zzz method_name(int, str, something else);
# argument = (int, str, something else);
# others = xxx yyy zzz method_name
"""
def method_list_getter(method_candidate_list):
    method_list = []
    for method_candidate in method_candidate_list:
        if method_candidate.endswith(');'):
            argument = '(' + method_candidate.split('(')[-1]
            argument = argument[:-1]
            others = method_candidate.split('(')[0]
            method_name = others.split(' ')[-1]
            method_list.append(method_name + argument)
            print method_name + arguments
    return method_list
"""
def method_list_getter(target):
    pattern = re.compile('^  \w.+\);$')
    method_index_list = [n for n,l in enumerate(target) if pattern.match(l)]
    method_list = []
    for x in method_index_list:
        method_dict = {}
        arg_start = target[x].index('(')
        arg_part = target[x][arg_start:-1]
        others = target[x][:arg_start]
        method_name = others.split(' ')[-1]
        print target[x]
        print arg_part
        print method_name
        print '\n'
        method_dict['name'] = method_name + arg_part
        #print method_dict['name']
        flag = 0
        for y in range(x+1, len(target) + 1):
            if (flag == 0) and (not target[y].endswith('LineNumberTable:')):
                method_dict['start'] = 'none'
                method_dict['end'] = 'none'
                break
            elif flag == 0:
                flag = 1
                continue
            if target[y].startswith('      line '):
                if not method_dict.has_key('start'):
                    method_dict['start'] = int(target[y].split(' ')[-2][:-1]) - 1
                else:
                    method_dict['end'] = int(target[y].split(' ')[-2][:-1]) + 1
            else:
                if not method_dict.has_key('end'):
                    method_dict['end'] = method_dict['start'] + 1
                break
        method_list.append(method_dict)
    return method_list

"""
f_java_class = open('java_class_link.csv', 'w')
f_class_method = open('class_method_link.csv', 'w')
csvWriter_jc = csv.writer(f_java_class, lineterminator='\n')
csvWriter_cm = csv.writer(f_class_method, lineterminator='\n')
"""
fp = open('java_class_method_link.csv', 'w')
csvWriter = csv.writer(fp, lineterminator='\n')

initial_path = '/Users/hideshi-s/Desktop/ehime/httpclient/httpclient5/target/classes'
#initial_path = '/Users/hideshi-s/Desktop/ehime/javaTest'
dir_counter = 0
for (directory, _, files) in os.walk(initial_path):
    num_file = len(files)
    file_counter = 0
    for f in files:
        if f.endswith('.class'):
            class_dict = class_info_getter(f, directory)
            javap_result_list = javap_exe(class_dict)
            java_dict = java_dict_getter(class_dict, javap_result_list[0])
            method_list = method_list_getter(javap_result_list)
            for method_dict in method_list:
                link_info = [java_dict['full path'], class_dict['full path'], method_dict['name'], method_dict['start'], method_dict['end']]
                csvWriter.writerow(link_info)
            """
            class_dict = class_info_getter(f, directory)
            class_detail_info_list = class_detail_info_getter(class_dict)
            java_dict = java_dict_getter(class_dict, class_detail_info_list[0])
            method_list = method_list_getter(class_detail_info_list[1:])
            link_info = [java_dict['full path'], class_dict['full path']]
            csvWriter_jc.writerow(link_info)
            for method in method_list:
                link_info = [class_dict['full path'], method]
                csvWriter_cm.writerow(link_info)
            """
        file_counter += 1
        print dir_counter, file_counter, num_file
    dir_counter += 1
#f_java_class.close()
#f_class_method.close()
fp.close()
