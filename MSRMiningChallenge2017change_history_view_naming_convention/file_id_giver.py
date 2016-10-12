# -*- coding: utf-8 -*-
'''
this script give IDs to the files.

input: (project_name).csv
output: files_production.txt
		files_test.txt
		file_id_list_production.csv
		file_id_list_test.csv
'''
import re
import sys
import csv
import os.path
import os
import subprocess
import csv

def id_giver_production():
	id = 1
	writer = csv.writer(file('file_id_list_production.csv', 'w'), lineterminator='\n')
	f = open('files_production.txt', 'r')
	line = f.readline()
	while line:
		file_info = []
		file_info.append(line.replace('\n', ''))
		file_info.append(id)
		writer.writerow(file_info)
		line = f.readline()
		id += 1
	f.close()
	return id

def id_giver_test(id):
	writer = csv.writer(file('file_id_list_test.csv', 'w'), lineterminator='\n')
	f = open('files_test.txt', 'r')
	line = f.readline()
	while line:
		file_info = []
		file_path = line.replace('\r', '')
		file_path = line.replace('\n', '')
		file_name = file_path.split('/')[-1]
		if file_name.endswith('Test.java'):
			file_name = file_name.split('Test.java')[0] + '.java' # hogeTest.java -> hoge.java
			query = '/'.join(file_path.replace('/src/test/java', '/src/main/java').split('/')[:-1]) + '/' + file_name
		elif file_name.startswith('Test'): # Testhoge.java -> hoge.java
			query = '/'.join(file_path.replace('/src/test/java', '/src/main/java').split('/')[:-1]) + '/' + file_name[4:]
		print query
		command = 'grep \"' + query + '\" file_id_list_production.csv'
		try:
			result = subprocess.check_output(command, shell=True)
			result.replace('\n', '')
			result.replace('\n', '')
			file_info.append(file_path)
			file_info.append(int(result.split(',')[-1]))
		except subprocess.CalledProcessError:
			file_info.append(file_path)
			file_info.append(id)
			id += 1
		writer.writerow(file_info)
		line = f.readline()
	f.close()
	return



def file_id_giver(pjt_name):
	command = 'grep \",production$\" ' + pjt_name + '.csv | cut -d\",\" -f2 | sort | uniq > files_production.txt'
	subprocess.call(command, shell=True)
	id = id_giver_production()
	command = 'grep \",test$\" ' + pjt_name + '.csv | cut -d\",\" -f2 | sort | uniq > files_test.txt'
	subprocess.call(command, shell=True)
	id_giver_test(id)
	command = 'cat file_id_list_production.csv file_id_list_test.csv > file_id_list.csv'
	subprocess.call(command, shell=True)
	return

if __name__ == '__main__':
	pjt_name = 'httpclient'
	file_id_giver(pjt_name)
