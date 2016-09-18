# -*- coding: utf-8 -*-
"""
This script parses index.html file created by Jacoco and calcurate line coverage.
"""
import subprocess
import sys
import os
import urllib2
import lxml.html
from lxml import etree

loc_list = []
uncovered_loc_list = []
pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/activejpa'
result = subprocess.check_output('find ' + pjt_path + ' | grep "jacoco/index\.html$"', shell=True)
result = result.replace('\r', '')
result_list = result.split('\n')
result_list.pop()
for html_path in result_list:
    print '_' + html_path + '_'
    root = lxml.html.parse(html_path).getroot()
    uncovered_loc_list.append(int(root.xpath('//*[@id="coveragetable"]/tfoot/tr/td[8]')[0].text.replace(',','')))
    loc_list.append(int(root.xpath('//*[@id="coveragetable"]/tfoot/tr/td[9]')[0].text.replace(',','')))
print 'line coverage: ' + str(100 * (float(sum(loc_list) - sum(uncovered_loc_list)) / sum(loc_list))) + '%'
