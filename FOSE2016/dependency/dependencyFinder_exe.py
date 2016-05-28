# -*- coding: utf-8 -*-
import subprocess
import os

pjt_path = '/Users/hideshi-s/Desktop/httpclient'
result = subprocess.check_output('find ' + pjt_path + ' | grep "\.jar$"', shell=True)
result = result.replace('\r', '')
result_list = result.split('\n')
result_list.pop()
for var in result_list:
    jar_path = var.split('/')
    target_index = jar_path.index('target')
    if jar_path[target_index+1].endswith('.jar'):
        if not (jar_path[-1].endswith('javadoc.jar') or jar_path[-1].endswith('sources.jar') or jar_path[-1].endswith('tests.jar')):
            print var
            #DependencyExtractor -xml -out df.xml httpclient5-5.0-alpha2-SNAPSHOT.jar
            jar_name = jar_path[-1][:-4] # fuga/hoge/piyo.jar -> piyo
            output_file_name = './' + jar_name + '.xml'
            os.system('DependencyExtractor -xml -out ' + output_file_name + ' ' + var)
