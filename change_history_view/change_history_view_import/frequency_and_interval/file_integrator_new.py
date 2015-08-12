# -*- coding: utf-8 -*-
"""
integrate (pjt_name).csv and file_id_list.csv and create change_history_view.csv

input: (pjt_name).csv
	   file_id_list.csv
output: change_history_view_new.csv.csv
"""
import re
import sys
import csv
import os.path
import os
import subprocess
import csv

def id_getter(file_name, id_list_file):
	command = "grep \"^" + file_name + ",\" " + id_list_file
	result = subprocess.check_output(command)
	id = result.split(",")[-1]
	id = id.replace("\n", "")
	return id

def checker(id):
	command = "grep \"," + id + "$\" file_id_list.csv"
	result = subprocess.check_output(command)
	result_list = result.split("\n")
	if len(result_list) == 3:
		flag = 1
	else:
		flag = 0
	return flag

def file_integrator(pjt_name, commit_info_file, id_list_file):
	result = subprocess.check_output('cat ' + commit_info_file + ' | wc -l', shell=True)
	result = result.replace("\n", "")
	num_lines = int(result.replace(" ", "")) - 1
	f = open(commit_info_file, "rb")
	writer = csv.writer(file("change_history_view_new.csv", "a"), lineterminator="\n")
	header = ["Date", "Author", "File", "Attribution", "ID"]
	writer.writerow(header)
	dataReader = csv.reader(f)
	flag = 0
	for data in dataReader:
		if flag == 0:
			flag += 1
			if commit_info_file == "pc_without_tc_without_bug.csv":
				continue
		date = data[0]
		date = date.replace("-", "/")
		author = data[1]
		file_name = data[2]
		if commit_info_file == "pc_with_tc_with_bug.csv":
			if data[3] == "test":
				attribution = data[3]
			elif data[3] == "introduce":
				attribution = data[3]
			else:
				attribution = "pc_with_bug"
		elif commit_info_file == "pc_with_tc_without_bug.csv":
			if data[3] == "test":
				attribution = data[3]
			elif data[3] == "introduce":
				attribution = data[3]
			else:
				attribution = "pc_without_bug"
		elif commit_info_file == "pc_without_tc_with_bug.csv":
			if data[3] == "introduce":
				attribution = data[3]
			else:
				attribution = "pc_with_bug"
		elif commit_info_file == "pc_without_tc_without_bug.csv":
			if data[3] == "introduce":
				attribution = data[3]
			else:
				attribution = "pc_without_bug"
		else:
			sys.exit("attribution error.")
		id = id_getter(file_name, id_list_file)
		#check_flag = checker(id)
		file_info = []
		file_info.append(date)
		file_info.append(author)
		file_info.append(file_name)
		file_info.append(attribution)
		file_info.append(id)
		writer.writerow(file_info)
		print str(flag) + " / " + str(num_lines) + " have been finished."
		flag += 1
	f.close()
	return

if __name__ == "__main__":
	argvs = sys.argv
	pjt_name = argvs[1]
	print "pc_with_tc_with_bug start"
	file_integrator(pjt_name, "pc_with_tc_with_bug.csv", "file_id_list_pc_with_tc_with_bug.csv")
	print "pc_with_tc_without_bug start"
	file_integrator(pjt_name, "pc_with_tc_without_bug.csv", "file_id_list_pc_with_tc_without_bug.csv")
	print "pc_without_tc_with_bug start"
	file_integrator(pjt_name, "pc_without_tc_with_bug.csv", "file_id_list_pc_without_tc_with_bug.csv")
	print "pc_without_tc_without_bug start"
	file_integrator(pjt_name, "pc_without_tc_without_bug.csv", "file_id_list_pc_without_tc_without_bug.csv")
