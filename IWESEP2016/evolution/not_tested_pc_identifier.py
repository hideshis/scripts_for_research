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
	except subprocess.CalledProcessError:
		print pc
	line = f.readline()
	pc = line.replace('\r', '')
	pc = pc.replace('\n', '')
f.close()
