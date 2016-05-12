# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import csv
import re

os.system('mkdir hogehoge')
initial_path = '/Users/hideshi-s/Desktop/httpclient/httpclient5/src/main/java'
result = subprocess.check_output('find ' + initial_path, shell=True)
result = result.replace('\r', '')
java_list = result.split('\n')
for java_file in java_list:
    if java_file.endswith('.java'):
        print java_file
        output_file = java_file.split('/')[-1] # foo/var/hoge.java -> hoge.java
        output_file = './hogehoge/' + output_file.replace('.java', '.csv') # hoge.java -> ./hogehoge/hoge.csv
        os.system('java -jar JavaMethodExtractor.jar ' + java_file + ' >' + output_file)
