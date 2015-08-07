# -*- coding: utf-8 -*-
"""
this script give IDs to the source codes.

input: (project_name).csv
output: files_production.txt
		file_id_list.csv
"""
import re
import sys
import csv
import os.path
import os
import subprocess
import csv

def id_giver_production():
	id = 1
	writer = csv.writer(file("file_id_list_production.csv", "w"), lineterminator="\n")
	f = open("files_production.txt", 'r')
	line = f.readline()
	while line:
		file_info = []
		file_info.append(line.replace("\n", ""))
		file_info.append(id)
		writer.writerow(file_info)
		line = f.readline()
		id += 1
	f.close()
	return id

def id_giver_test(id):
	writer = csv.writer(file("file_id_list_test.csv", "w"), lineterminator="\n")
	f = open("files_test.txt", 'r')
	line = f.readline()
	while line:
		file_info = []
		file_name = line.replace("\n", "")
		if file_name.endswith("Test.java"):
			query = file_name.split("Test.java")[0]
			query += ".java"
		elif file_name.endswith("Tests.java"):
			query = file_name.split("Tests.java")[0]
			query += ".java"
		command = "grep \"^" + query + ",\" file_id_list_production.csv"
		try:
			result = subprocess.check_output(command)
			result.replace("\n", "")
			result.replace("\n", "")
			file_info.append(file_name)
			file_info.append(int(result.split(",")[-1]))
		except subprocess.CalledProcessError:
			file_info.append(file_name)
			file_info.append(id)
			id += 1
		writer.writerow(file_info)
		line = f.readline()
	f.close()
	return



def file_id_giver(pjt_name):
	"""
	command = "grep \",production$\" " + pjt_name + ".csv | cut -d',' -f3 | sort | uniq > files_production.txt"
	subprocess.call(command, shell=True)
	id = id_giver_production()
	command = "grep \",test$\" " + pjt_name + ".csv | cut -d',' -f3 | sort | uniq > files_test.txt"
	subprocess.call(command, shell=True)
	id_giver_test(id)
	command = "cat file_id_list_production.csv file_id_list_test.csv > file_id_list.csv"
	subprocess.call(command, shell=True)
	"""
	command = "grep \",production$\|,test$\" " + pjt_name + "_all.csv | cut -d',' -f4 | sort | uniq > files_production.txt"
	subprocess.call(command, shell=True)
	id = id_giver_production()
	command = "mv file_id_list_production.csv file_id_list.csv"
	subprocess.call(command, shell=True)
	return

if __name__ == "__main__":
	argvs = sys.argv
	pjt_name = argvs[1]
	file_id_giver(pjt_name)
