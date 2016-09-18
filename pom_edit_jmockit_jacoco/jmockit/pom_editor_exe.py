# -*- coding: utf-8 -*-
import subprocess
import sys
import os

#pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/httpclient'
#pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/activejpa'
pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/basex'
result = subprocess.check_output('find ' + pjt_path + ' | grep "pom\.xml$"', shell=True)
result = result.replace('\r', '')
result_list = result.split('\n')
result_list.pop()
for pom_file in result_list:
    print 'now on eiditing ' + pom_file + '...'
    os.system('python pom_editor.py ' + pom_file)
