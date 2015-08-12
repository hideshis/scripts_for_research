# -*- coding: utf-8 -*-
"""
integrate (pjt_name).csv and file_id_list.csv and create change_history_view.csv

input: (pjt_name).csv
	   file_id_list.csv
output: change_history_view.csv
"""
import os
import csv
import sys
import math
from datetime import datetime
import subprocess

def median_getter(target):
	target.sort()
	if len(target) >= 1:
		return target[len(target) / 2]
	else:
		return -1

def frequency_getter(file_name, attribution):
	cmd = 'grep ",' + attribution + '," ' + file_name + ' | cut -d\',\' -f5 | sort | uniq'
	result = subprocess.check_output(cmd, shell=True)
	result = result.replace("\r", "")
	id_list = result.split("\n")
	frequency_list = []
	for x in id_list:
		cmd = 'grep ",' + attribution + ',' + x + '" ' + file_name + ' | wc -l'
		result = subprocess.check_output(cmd, shell=True)
		result = result.replace("\n", "")
		result = result.replace(" ", "")
		frequency = int(result)
		frequency_list.append(frequency)
	return median_getter(frequency_list)

def hogehoge1(file_name, when):
	return_list = []
	return_list.append(frequency_getter(file_name, "pc_with_bug"))
	return_list.append(frequency_getter(file_name, "pc_without_bug"))
	return_list.append(frequency_getter(file_name, "pc_with_bug-test"))
	return_list.append(frequency_getter(file_name, "pc_without_bug-test"))
	return return_list

year_list = ["2003" ,"2004" ,"2005" ,"2006" ,"2007" ,"2008" ,"2009" ,"2010" ,"2011" ,"2012" ,"2013" ,"2014" ,"2015"]
writer = csv.writer(file("result.csv", 'w'), lineterminator="\n")
header = ["period", "pc_with_bug", "pc_without_bug", "pc_with_bug_test", "pc_without_bug_test", "#bug"]
writer.writerow(header)
for year in year_list:
	if year != "2003":
		file_name = 'chv_' + year + '_01_06.csv'
		print file_name
		frequency_list = hogehoge1(file_name, year + "_01_06")
		kakikomi_list = []
		kakikomi_list.append(year + '_01_06')
		kakikomi_list.append(frequency_list[0])
		kakikomi_list.append(frequency_list[1])
		kakikomi_list.append(frequency_list[2])
		kakikomi_list.append(frequency_list[3])
		try:
			result = subprocess.check_output('grep ",introduce," ' + file_name + ' | wc -l', shell=True)
			result = result.replace("\n", "")
			result = result.replace(" ", "")
		except subprocess.CalledProcessError:
			result = "0"
		kakikomi_list.append(int(result))
		writer.writerow(kakikomi_list)
	file_name = 'chv_' + year + '_07_12.csv'
	print file_name
	frequency_list = hogehoge1(file_name, year + "_07_12")
	kakikomi_list = []
	kakikomi_list.append(year + '_07_12')
	kakikomi_list.append(frequency_list[0])
	kakikomi_list.append(frequency_list[1])
	kakikomi_list.append(frequency_list[2])
	kakikomi_list.append(frequency_list[3])
	try:
		result = subprocess.check_output('grep ",introduce," ' + file_name + ' | wc -l', shell=True)
		result = result.replace("\n", "")
		result = result.replace(" ", "")
	except subprocess.CalledProcessError:
		result = "0"
	kakikomi_list.append(int(result))
	writer.writerow(kakikomi_list)
