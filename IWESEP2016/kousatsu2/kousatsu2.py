# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

def updator(tc_name, file_name):
	os.chdir("./evolution_info")
	try:
		result = subprocess.check_output('grep ",production" ' + file_name, shell=True)
		result = result.replace("\r", "")
		result = result.split("\n")[0]
		pc_name = result.split(",")[-2]
		query = tc_name + "," + pc_name
		result = subprocess.check_output('grep "' + query + '" ../bug_info_detail.csv', shell=True)
		result = result.replace("\r", "")
		result_list = result.split("\n")
		result_list.pop()
		for x in result_list:
			bug_introducing_time = x.split(",")[-1]
			query = "hoge," + bug_introducing_time + ",hoge,hoge,bug"
			os.system("echo " + query + ">>" + file_name)
			os.system('sort -t, -nk2,2 ' + file_name + ' | uniq >tmp.csv')
			os.system('mv tmp.csv ' + file_name)
	except subprocess.CalledProcessError:
		tc_name = tc_name
	os.chdir("..")
	return

f = open("slt_si_hr.csv", 'r')
tc_name = f.readline()
tc_name = tc_name.split(',')[0]
os.system('rm -Rf ./evolution_info')
os.system('mkdir evolution_info')
while tc_name:
	query = tc_name.replace("/", "_")
	query = query.replace(".", "_")
	result = subprocess.check_output('find ../co_evolution/evolution_info -name "' + query + '__*.csv"', shell=True)
	result = result.replace('\r', '')
	file_list = result.split('\n')
	file_list.pop()
	for file_name in file_list:
		os.system("cp " + file_name + " ./evolution_info")
		updator(tc_name, file_name.split("/")[-1])
	tc_name = f.readline()
	tc_name = tc_name.split(',')[0]
