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

def hogehoge1(file_name, when):
	cmd = 'grep -v ",introduce," ' + file_name +' | grep -v ",introduce," | grep -v ",pc_without_bug-test," | grep -v ",pc_with_bug-test," | grep -v ",Attribution," | sort -t , -k 5n,5 -k 1n,1 > chv_for_commit_interval_checking_sorted' + when + '_pc.csv'
	os.system(cmd)
	f = open("chv_for_commit_interval_checking_sorted" + when + "_pc.csv", "r")
	dataReader = csv.reader(f)
	pc_id = 0
	td_pc_with_bug = []
	td_pc_without_bug = []
	td_tmp = []
	for data in dataReader:
		if pc_id != data[-1]:
			if pc_id == 0:
				pc_id = data[-1]
				date = data[0]
				attribution = data[-2]
				first_date = datetime.strptime(date, '%Y/%m/%d')
			else:
				if len(td_tmp) >= 1:
					td_ave = sum(td_tmp) / len(td_tmp)
					if attribution == "pc_with_bug":
						td_pc_with_bug.append(td_ave)
					elif attribution == "pc_without_bug":
						td_pc_without_bug.append(td_ave)
					else:
						sys.exit("error")
				td_tmp = []
				date = data[0]
				attribution = data[-2]
				pc_id = data[-1]
				first_date = datetime.strptime(date, '%Y/%m/%d')
		else:
			date = data[0]
			attribution = data[-2]
			pc_id = data[-1]
			last_date = datetime.strptime(date, '%Y/%m/%d')
			delta = last_date - first_date
			td_tmp.append(delta.days)
			first_date = last_date
	if len(td_pc_with_bug) >= 1:
		ave1 = sum(td_pc_with_bug) / len(td_pc_with_bug)
	else:
		ave1 = -1
	if len(td_pc_without_bug) >= 1:
		ave2 = sum(td_pc_without_bug) / len(td_pc_without_bug)
	else:
		ave2 = -1
	print "commmit interval for pc_with_bug-pc: " + str(ave1) + " " + str(median_getter(td_pc_with_bug))
	print "commmit interval for pc_without_bug-pc: " + str(ave2) + " " + str(median_getter(td_pc_without_bug))
	return_list = []
	return_list.append(median_getter(td_pc_with_bug))
	return_list.append(median_getter(td_pc_without_bug))
	return return_list

def hogehoge2(file_name, when):
	cmd = 'grep -v ",introduce," ' + file_name + ' | grep -v ",introduce," | grep -v ",pc_without_bug," | grep -v ",pc_with_bug," | grep -v ",Attribution," | sort -t , -k 5n,5 -k 1n,1 > chv_for_commit_interval_checking_sorted' + when + '_tc.csv'
	os.system(cmd)
	f = open("chv_for_commit_interval_checking_sorted" + when + "_tc.csv", "r")
	dataReader = csv.reader(f)
	pc_id = 0
	td_pc_with_bug = []
	td_pc_without_bug = []
	td_tmp = []
	for data in dataReader:
		if pc_id != data[-1]:
			if pc_id == 0:
				pc_id = data[-1]
				date = data[0]
				attribution = data[-2]
				first_date = datetime.strptime(date, '%Y/%m/%d')
			else:
				if len(td_tmp) >= 1:
					td_ave = sum(td_tmp) / len(td_tmp)
					if attribution == "pc_with_bug-test":
						td_pc_with_bug.append(td_ave)
					elif attribution == "pc_without_bug-test":
						td_pc_without_bug.append(td_ave)
					else:
						sys.exit("error")
				td_tmp = []
				date = data[0]
				attribution = data[-2]
				pc_id = data[-1]
				first_date = datetime.strptime(date, '%Y/%m/%d')
		else:
			date = data[0]
			attribution = data[-2]
			pc_id = data[-1]
			last_date = datetime.strptime(date, '%Y/%m/%d')
			delta = last_date - first_date
			td_tmp.append(delta.days)
			first_date = last_date
	if len(td_pc_with_bug) >= 1:
		ave1 = sum(td_pc_with_bug) / len(td_pc_with_bug)
	else:
		ave1 = -1
	if len(td_pc_without_bug) >= 1:
		ave2 = sum(td_pc_without_bug) / len(td_pc_without_bug)
	else:
		ave2 = -1
	print "commmit interval for pc_with_bug-test: " + str(ave1) + " " + str(median_getter(td_pc_with_bug))
	print "commmit interval for pc_without_bug-test: " + str(ave2) + " " + str(median_getter(td_pc_without_bug))
	return_list = []
	return_list.append(median_getter(td_pc_with_bug))
	return_list.append(median_getter(td_pc_without_bug))
	return return_list

year_list = ["2003" ,"2004" ,"2005" ,"2006" ,"2007" ,"2008" ,"2009" ,"2010" ,"2011" ,"2012" ,"2013" ,"2014" ,"2015"]
writer = csv.writer(file("result.csv", 'w'), lineterminator="\n")
header = ["period", "pc_with_bug", "pc_without_bug", "pc_with_bug_test", "pc_without_bug_test", "#bug"]
writer.writerow(header)
for year in year_list:
	if year != "2003":
		file_name = 'chv_' + year + '_01_06.csv'
		hogehoge1_return = hogehoge1(file_name, year + "_01_06")
		hogehoge2_return = hogehoge2(file_name, year + "_01_06")
		kakikomi_list = []
		kakikomi_list.append(year + '_01_06')
		kakikomi_list.append(int(hogehoge1_return[0]))
		kakikomi_list.append(int(hogehoge1_return[1]))
		kakikomi_list.append(int(hogehoge2_return[0]))
		kakikomi_list.append(int(hogehoge2_return[1]))
		try:
			result = subprocess.check_output('grep ",introduce," ' + file_name + ' | wc -l', shell=True)
			result = result.replace("\n", "")
			result = result.replace(" ", "")
		except subprocess.CalledProcessError:
			result = "0"
		kakikomi_list.append(int(result))
		writer.writerow(kakikomi_list)
	file_name = 'chv_' + year + '_07_12.csv'
	hogehoge1_return = hogehoge1(file_name, year + "_07_12")
	hogehoge2_return = hogehoge2(file_name, year + "_07_12")
	kakikomi_list = []
	kakikomi_list.append(year + '_07_12')
	kakikomi_list.append(int(hogehoge1_return[0]))
	kakikomi_list.append(int(hogehoge1_return[1]))
	kakikomi_list.append(int(hogehoge2_return[0]))
	kakikomi_list.append(int(hogehoge2_return[1]))
	try:
		result = subprocess.check_output('grep ",introduce," ' + file_name + ' | wc -l', shell=True)
		result = result.replace("\n", "")
		result = result.replace(" ", "")
	except subprocess.CalledProcessError:
		result = "0"
	kakikomi_list.append(int(result))
	writer.writerow(kakikomi_list)
