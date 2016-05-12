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

def method_list_getter(target):
    # extract line numbers which declare method.
    #pattern = re.compile('^  \w.+\);$')
    #method_index_list = [n for n,l in enumerate(target) if pattern.match(l)]
    method_candidate_index_list = [n for n,l in enumerate(target) if (('(' in l) and (')' in l) and l.endswith(';'))]
    method_index_list = [n for n in method_candidate_index_list if ('LineNumberTable:' in target[n+1])]
    method_list = []
    for x in method_index_list:
        method_dict = {}
        arg_part = target[x][target[x].index('('):target[x].index(')')+1]
        others = target[x][:target[x].index('(')]
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
                    method_dict['end'] = int(target[y].split(' ')[-2][:-1]) + 1
                else:
                    method_dict['end'] = int(target[y].split(' ')[-2][:-1]) + 1
            else:
                """
                if not method_dict.has_key('end'):
                    method_dict['end'] = method_dict['start'] + 1
                """
                break
        method_list.append(method_dict)
    return method_list

fp = open('java_class_method_link.csv', 'w')
csvWriter = csv.writer(fp, lineterminator='\n')

initial_path = '/Users/hideshi-s/Desktop/ehime/httpclient/httpclient/target/classes'
#initial_path = '/Users/hideshi-s/Desktop/ehime/javaTest'
dir_counter = 0
for (directory, _, files) in os.walk(initial_path):
    num_file = len(files)
    file_counter = 0
    for f in files:
        if f.endswith('.class'):
            # class_dict = {'name':f, 'path':directory, 'full path':directory+'/'+f}
            class_dict = class_info_getter(f, directory)
            # execute 'javap -l -private class_dict['full path']'
            javap_result_list = javap_exe(class_dict)
            java_dict = java_dict_getter(class_dict, javap_result_list[0])
            method_list = method_list_getter(javap_result_list)
            for method_dict in method_list:
                link_info = [java_dict['full path'], class_dict['full path'], method_dict['name'], method_dict['start'], method_dict['end']]
                csvWriter.writerow(link_info)
        file_counter += 1
        print dir_counter, file_counter, num_file
    dir_counter += 1
fp.close()
