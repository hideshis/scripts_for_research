# -*- coding: utf-8 -*-
import sys
import subprocess

class bug_info:
    def __init__(self, bug_info_list):
        self.file_name = bug_info_list[0]
        self.begin_line = bug_info_list[1]
        self.end_line = bug_info_list[2]
        self.bug_introducing_commit = bug_info_list[3]
        self.method_name_list = self.get_method_name()
        self.is_covered = False

    def get_method_name(self):
        file_name_splitted = self.file_name.split('/')
        file_name_splitted = file_name_splitted[file_name_splitted.index('org'):]
        file_name_converted = '.'.join(file_name_splitted)
        try:
            result = subprocess.check_output('grep ' + file_name_converted + ' ./file_class_method_link/file_class_method_converted.csv | cut -d\'|\' -f3,4,5', shell=True)
            result_list = result.replace('\r', '').replace('\n', '|').split('|').pop()
            flag = 0
            method_dict_list = []
            for i in range(len(result_list)):
                if i%3 == 0:
                    if flag == 0:
                        flag += 1
                    else:
                        method_dict_list.append(method_dict)
                    method_dict = {}
                    method_dict['method_name'] = result_list[i]
                elif i%3 == 1:
                    method_dict['begin_line'] = result_list[i]
                else:
                    method_dict['end_line'] = result_list[i]
            method_name_list = []
            for method_dict in method_dict_list:
                if not ((self.begin_line > method_dict['end_line']) or (self.end_line < method_dict['begin_line'])):
                    method_name_list.append(method_dict['method_name'])
            return method_name_list
        except subprocess.CalledProcessError:
            return []

class callee_info:
    def __init__(self):
        self.method_name = ""
        self.is_covered = False

if __name__ == "__main__":
    f = open('./bug_location/bug_location_info.csv', 'r')
    for line in f.readlines():
        bug_info = bug_info(line.replace('\r', '').replace('\n', '').split(','))

        sys.exit()
