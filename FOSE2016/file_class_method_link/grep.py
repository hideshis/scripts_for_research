# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import csv

result = subprocess.check_output('cut -d"|" -f3 ./file_class_method_converted.csv', shell=True)
result = result.replace('\r', '')
method_list = result.split('\n')
exist_counter = 0
non_exist_counter = 0
for method in method_list:
    try:
        if '[]' in method:
            method = method.replace('[]', '\[\]')
        result = subprocess.check_output('grep "' + method + '" ../dependency/feature_list.csv', shell=True)
        exist_counter += 1
    except subprocess.CalledProcessError:
        print method
        non_exist_counter += 1
print exist_counter, non_exist_counter
