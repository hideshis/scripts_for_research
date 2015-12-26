# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

os.chdir("./evolution_info")
csv_list = os.listdir("./")
rank = []
for csv_file in csv_list:
	result = subprocess.check_output('grep "bug" ' + csv_file + " | wc -l", shell=True)
	result = result.replace('\r', '')
	result = result.replace('\n', '')
	result = result.replace(' ', '')
	rank.append([int(result), csv_file])
rank.sort(reverse=True)
for x in range(10):
	print rank[x]
os.chdir("..")
