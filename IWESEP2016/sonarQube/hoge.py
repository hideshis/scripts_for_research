# -*- coding: utf-8 -*-
import re
import sys
import csv
import os.path
import os
import datetime
import subprocess
import sonar_analyzer

def git_clone_and_checkouter(commit_hash):
	os.system('rm -Rf target')
	os.system('git clone https://github.com/apache/httpclient.git target')
	os.chdir('./target')
	os.system('git checkout ' + commit_hash)
	os.chdir('..')
	return


def tc_list_getter(pattern):
	result = subprocess.check_output('cat ' + pattern + ' | cut -d"," -f1', shell=True)
	result = result.replace('\r', '')
	tc_list = result.split('\n')
	tc_list.pop()
	return tc_list

def commit_hash_getter():
	result = subprocess.check_output('cat commit_hash_list.txt | cut -d" " -f1', shell=True)
	result = result.replace('\r', '')
	commit_hash_list = result.split('\n')
	commit_hash_list.pop()
	return commit_hash_list

def fild_all_files(directory):
	for root, dirs, files in os.walk(directory):
		yield root
		for file in files:
			yield os.path.join(root, file)

def executable_tc_list_getter(tc_list):
	file_list = []
	for file in fild_all_files('./target'):
		file = file.replace('./target/', '')
		file_list.append(file)
	tc_list = tc_list + file_list
	s = set()
	executable_tc_list = [x for x in tc_list if x in s or s.add(x)]
	return executable_tc_list

def test_sonar_execution():
	os.chdir('./target')
	os.system('mvn clean org.jacoco:jacoco-maven-plugin:0.7.4.201502262128:prepare-agent install -Dmaven.test.failure.ignore=true')
	os.system('mvn sonar:sonar > sonar_log.txt')
	os.system('mv sonar_log.txt ..')
	os.chdir('..')
	return

def execution_result_checker():
	query = '\[INFO\] BUILD SUCCESS'
	try:
		result = subprocess.check_output('grep "' + query + '" sonar_log.txt', shell=True)
		return "success"
	except subprocess.CalledProcessError:
	 	return "failure"
	sys.exit()
	return

sonar_analyzer.analysis()
sys.exit()
commit_hash_list = commit_hash_getter()
for commit_hash in commit_hash_list:
	git_clone_and_checkouter(commit_hash)
	test_sonar_execution()
	execution_result = execution_result_checker()
	if execution_result == "failure":
		continue
	else:
		print commit_hash
		print execution_result
		sonar_analyzer.analysis()
	sys.exit()

"""
pattern_list = os.listdir('./')
for pattern in pattern_list:
	if not pattern.endswith(".csv"):
		continue
	tc_list = tc_list_getter(pattern)
	commit_hash_list = commit_hash_getter()
	for commit_hash in commit_hash_list:
		git_clone_and_checkouter(commit_hash)
		executable_tc_list = executable_tc_list_getter(tc_list)
		if len(executable_tc_list) == 0:
			continue
		test_sonar_execution(executable_tc_list)
		execution_result = execution_result_checker()
		print execution_result
		if execution_result == "failure":
			continue
		else:
			print pattern
			print commit_hash
			print executable_tc_list
			print execution_result
		sys.exit()
"""
