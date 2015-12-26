# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv
import numpy

def pc_counter(tc_name, file_name):
	os.chdir("./evolution_info")
	result = subprocess.check_output('grep ",production" ' + file_name + " | wc -l", shell=True)
	result = result.replace('\r', '')
	result = result.replace('\n', '')
	result = result.replace(' ', '')
	os.chdir("..")
	return int(result)

def tc_counter(tc_name, file_name):
	os.chdir("./evolution_info")
	result = subprocess.check_output('grep ",test" ' + file_name + " | wc -l", shell=True)
	result = result.replace('\r', '')
	result = result.replace('\n', '')
	result = result.replace(' ', '')
	os.chdir("..")
	return int(result)

f = open("slt_si_hr_dripped.csv", 'r')
tc_name = f.readline()
tc_name = tc_name.replace('\r', '')
tc_name = tc_name.replace('\n', '')
os.system('rm -Rf ./evolution_info')
os.system('mkdir evolution_info')
ave_pc_mod_list = []
ave_tc_mod_list = []
production_modification_list = []
test_modification_list = []
while tc_name:
	query = tc_name.replace("/", "_")
	query = query.replace(".", "_")
	result = subprocess.check_output('find ../co_evolution/evolution_info -name "' + query + '__*.csv"', shell=True)
	result = result.replace('\r', '')
	file_list = result.split('\n')
	file_list.pop()
	#production_modification_list = []
	#test_modification_list = []
	for file_name in file_list:
		os.system("cp " + file_name + " ./evolution_info")
		production_modification_list.append(pc_counter(tc_name, file_name.split("/")[-1]))
		test_modification_list.append(tc_counter(tc_name, file_name.split("/")[-1]))
	#hoge_pc = float(sum(production_modification_list)) / float(len(production_modification_list))
	#hoge_tc = float(sum(test_modification_list)) / float(len(test_modification_list))
	#ave_pc_mod_list.append(hoge_pc)
	#ave_tc_mod_list.append(hoge_tc)
	#print tc_name
	#print hoge_pc, hoge_tc, float(hoge_pc / hoge_tc)
	tc_name = f.readline()
	tc_name = tc_name.replace('\r', '')
	tc_name = tc_name.replace('\n', '')
#data_pc = numpy.array(ave_pc_mod_list)
#data_tc = numpy.array(ave_tc_mod_list)
data_pc = numpy.array(production_modification_list)
data_tc = numpy.array(test_modification_list)
print numpy.median(data_pc), numpy.median(data_tc), float(numpy.median(data_pc)/numpy.median(data_tc))
