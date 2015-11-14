# -*- coding: utf-8 -*-
"""
"""
import re
import sys
import csv
import os.path
import os
import datetime

argvs = sys.argv
pjt_name = argvs[1]
f = open('pc_tc_link_info.csv', 'r')
lines = f.readlines()
f.close()
os.system('mkdir evolution_info')
for line in lines:
	line = line.replace("\r", "")
	line = line.replace("\n", "")
	source_code_list = line.split(",")
	file_name = source_code_list[0]
	file_name = file_name.replace("/", "_")
	file_name = file_name.replace(".", "_")
	file_name = file_name + ".csv"
	os.system('grep "' + source_code_list[0] + '" ' + pjt_name + '_all.csv>>' + file_name)
	os.system('grep "' + source_code_list[0] + '" imported_pc_list.csv | cut -d, -f1,2,3,4,5 >>' + file_name)
	"""
	for source_code in source_code_list:
		os.system('grep "' + source_code + '" ' + pjt_name + '_all.csv>>' + file_name)
	"""
	os.system('sort -t, -nk2,2 ' + file_name + ' >tmp.csv')
	os.system('mv tmp.csv ' + file_name)
	os.system('mv ' + file_name + ' ./evolution_info')
