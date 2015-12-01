# -*- coding: utf-8 -*-
"""
this script identifies which product codes don't have test codes.
"""
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess

f = open('pc_list.txt', 'r')
line = f.readline()
pc = line.replace('\r', '')
pc = pc.replace('\n', '')
while line:
	try:
		result = subprocess.check_output('grep "' + pc + '" pc_tc_link_info.csv', shell=True)
		os.system('echo ' + pc + '>>pc_with_test_list.txt')
	except subprocess.CalledProcessError:
		os.system('echo ' + pc + '>>pc_without_test_list.txt')
	line = f.readline()
	pc = line.replace('\r', '')
	pc = pc.replace('\n', '')
f.close()
