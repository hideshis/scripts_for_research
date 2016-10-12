# -*- coding: utf-8 -*-
"""
this script give IDs to the files.

input: (project_name).csv
output: files_production.txt
		files_test.txt
		file_id_list_production.csv
		file_id_list_test.csv
"""
import re
import sys
import csv
import os.path
import os
import subprocess
import csv

def id_getter(file_name):
	command = "grep \"^" + file_name + ",\" file_id_list.csv"
	result = subprocess.check_output(command, shell=True)
	id = result.split(",")[-1]
	id = id.replace("\n", "")
	return id

def checker(id):
	command = "grep \"," + id + "$\" file_id_list.csv"
	result = subprocess.check_output(command, shell=True)
	result = result.replace('\r', '')
	result_list = result.split('\n')
	if len(result_list) == 3:
		flag = 1
	else:
		flag = 0
	return flag

def file_integrator(pjt_name):
	backlog = subprocess.check_output('wc -l ' + pjt_name + '.csv', shell=True).split(' ')[-2]
	f = open(pjt_name+".csv", "rb")
	writer = csv.writer(file("change_history_view.csv", "w"), lineterminator="\n")
	header = ["Date", "File", "Attribution", "ID"]
	writer.writerow(header)
	dataReader = csv.reader(f)
	flag = 0
	for data in dataReader:
		if flag == 0:
			flag += 1
			continue
		date = data[0]
		file_name = data[1]
		attribution = data[2]
		id = id_getter(file_name)
		check_flag = checker(id)
		# if the file doesn't have corresponding test/product code, then skip to the next loop.
		if check_flag == 0:
			print str(flag) + " / " + backlog + " have been finished."
			flag += 1
			continue
		file_info = []
		file_info.append(date)
		file_info.append(file_name)
		file_info.append(attribution)
		file_info.append(id)
		writer.writerow(file_info)
		print str(flag) + " / " + backlog + " have been finished."
		flag += 1
	f.close()
	return

if __name__ == "__main__":
	pjt_name = "httpclient"
	file_integrator(pjt_name)
