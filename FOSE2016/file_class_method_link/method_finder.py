# -*- coding: utf-8 -*-
import os
import sys
import subprocess

#f = open('hogehoge.csv', 'r')
f = open('class_list.txt', 'r')
line = f.readline()
line = line.replace('\r', '')
line = line.replace('\n', '')
found_counter = 0
not_found_counter = 0
while line:
    #class_name = line.split(',')[1]
    #method_name = line.split(',')[2]
    #os.system('grep "' + class_name + '" ../dependency/class_list.txt')
    #os.system('grep "' + line + '" ../dependency/class_list.txt')
    try:
        result = subprocess.check_output('grep "' + line + '" ../dependency/class_list.txt', shell=True)
        found_counter += 1
    except subprocess.CalledProcessError:
        not_found_counter += 1
    line = f.readline()
    line = line.replace('\r', '')
    line = line.replace('\n', '')
print found_counter, not_found_counter
