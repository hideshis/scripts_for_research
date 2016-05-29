# -*- coding: utf-8 -*-
import subprocess
import os

pjt_path = '/Users/hideshi-s/Desktop/httpclient'
result = subprocess.check_output('find ' + pjt_path + ' | grep "\.jar$"', shell=True)
result = result.replace('\r', '')
result_list = result.split('\n')
result_list.pop()
for jar_file in result_list:
    jar_path = jar_file.split('/')
    target_index = jar_path.index('target')
    if jar_path[target_index+1].endswith('.jar'):
        if not (jar_path[-1].endswith('javadoc.jar') or jar_path[-1].endswith('sources.jar') or jar_path[-1].endswith('tests.jar')):
            print jar_file
            #DependencyExtractor -xml -out df.xml httpclient5-5.0-alpha2-SNAPSHOT.jar
            component_name = jar_path[target_index-1]
            DF_report_name = './' + component_name + '.xml'
            DF_report_parsed_name = './' + component_name + '.csv'
            print 'finding dependencies...'
            os.system('DependencyExtractor -xml -out ' + DF_report_name + ' ' + jar_file)
            print 'parsing dependencyFinder report...'
            os.system('python df_xml_parser.py ' + DF_report_name + ' ' + DF_report_parsed_name)
