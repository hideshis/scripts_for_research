# -*- coding: utf-8 -*-
"""
This script parses index.html files created by Jacoco and calcurate line coverage.
"""
import subprocess
import sys
import os
import urllib2
import lxml.html
from lxml import etree

f_write = open('coverage_info.csv', 'w')
csvWriter = csv.writer(f_write, lineterminator='\n')
f_read = open('maven_projects.csv', 'r')
pjt_id = f_read.readline().replace('\r', '').replace('\n', '')
pjt_name = pjt_id.split('/')[-1]
pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/' + pjt_name
loc_list = []
uncovered_loc_list = []
while pjt_name:
    result = subprocess.check_output('find ' + pjt_path + ' | grep "jacoco/index\.html$"', shell=True)
    result = result.replace('\r', '')
    result_list = result.split('\n')
    result_list.pop()
    for html_path in result_list:
        print '_' + html_path + '_'
        root = lxml.html.parse(html_path).getroot()
        uncovered_loc_list.append(int(root.xpath('//*[@id="coveragetable"]/tfoot/tr/td[8]')[0].text.replace(',','')))
        loc_list.append(int(root.xpath('//*[@id="coveragetable"]/tfoot/tr/td[9]')[0].text.replace(',','')))
    print pjt_id + '->line coverage: ' + str(100 * (float(sum(loc_list) - sum(uncovered_loc_list)) / sum(loc_list))) + '%'
    coverage_info = []
    coverage_info.append(pjt_id)
    coverage_info.append(100 * (float(sum(loc_list) - sum(uncovered_loc_list)) / sum(loc_list)))
    csvWriter.writerow(coverage_info)
    pjt_id = f_read.readline().replace('\r', '').replace('\n', '')
    pjt_name = pjt_id.split('/')[-1]
    pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/' + pjt_name
    loc_list = []
    uncovered_loc_list = []
f_write.close()
f_read.close()
