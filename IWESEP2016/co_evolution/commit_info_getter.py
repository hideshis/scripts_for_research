# -*- coding: utf-8 -*-
"""
"""
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess

def pc_name_list_getter(tc_name):
	result = subprocess.check_output('grep ",' + tc_name + '" pc_tc_link_info.csv', shell=True)
	result = result.replace('\r', '')
	result_list = result.split('\n')
	result_list.pop()
	pc_name_list = []
	for pc_name in result_list:
		pc_name = pc_name.split(',')[0]
		pc_name_list.append(pc_name)
	return pc_name_list

def lifetime_getter(tc_name):
	lifetime = {}
	result = subprocess.check_output('egrep "^' + tc_name + '," target_tc_lifetime_frequency.csv', shell=True)
	lifetime['born'] = int(result.split(',')[4])
	lifetime['dead'] = int(result.split(',')[5])
	return lifetime

def pc_commit_getter(pjt_name, pc_name, lifetime):
	result = subprocess.check_output('grep ",' + pc_name + '," ' + pjt_name + '_all.csv', shell=True)
	result = result.replace('\r', '')
	pc_commit_list = result.split('\n')
	pc_commit_list.pop()
	black_list = []
	for pc_commit in pc_commit_list:
		date = int(pc_commit.split(',')[1])
		if (lifetime['dead'] >= date) and (date >= lifetime['born']):
			black_list = black_list
		else:
			black_list.append(pc_commit)
	print black_list
	for black_listed_commit in black_list:
		pc_commit_list.remove(black_listed_commit)
	return pc_commit_list

def commit_getter(pjt_name, pc_name_list, tc_name, lifetime, file_name):
	f = open(file_name, 'w')
	for pc_name in pc_name_list:
		pc_commit_list = pc_commit_getter(pjt_name, pc_name, lifetime)
		for pc_commit in pc_commit_list:
			f.write(pc_commit + '\n')
	f.close()
	for pc_name in pc_name_list:
		os.system('grep ",' + tc_name + '," target_all.csv >>' + file_name)
	os.system('sort -t, -nk2,2 ' + file_name + ' | uniq >tmp.csv')
	os.system('mv tmp.csv ' + file_name)
	os.system('mv ' + file_name + ' ./evolution_info')
	return


pjt_name = "target"
f = open('importing_tc_list.txt', 'r')
lines = f.readlines()
f.close()
os.system('mkdir evolution_info')
for tc_name in lines:
	tc_name = tc_name.replace("\r", "")
	tc_name = tc_name.replace("\n", "")
	file_name = tc_name.replace("/", "_")
	file_name = file_name.replace(".", "_")
	file_name = file_name + ".csv"
	pc_name_list = pc_name_list_getter(tc_name)
	lifetime = lifetime_getter(tc_name)
	commit_getter(pjt_name, pc_name_list, tc_name, lifetime, file_name)
