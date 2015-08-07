# -*- coding: utf-8 -*-
"""
this script extracts commit info.
the commits are memorized only if one ore more java files are commited.
the log file is extracted by the following command:
	git log --pretty=format:"commit:%H%nauthor:%an%ndate:%at" --name-only > log_(project_name).txt
this script is called by auto_top.sh

input: log_(project_name).txt
output: (project_name).csv
		(project_name)_tc.csv
		(project_name)_all.csv
"""
import re
import sys
import csv
import os.path
import os
import datetime

def csv_writer_tc(pjt_name, commit_hash, files):
	f = open(pjt_name + '_tc.csv', 'a')
	csvWriter = csv.writer(f, lineterminator="\n")
	size = os.path.getsize(pjt_name + '.csv')
	if size == 0:
		title = ["Commit_hash", "File"]
		csvWriter.writerow(title)
	file_list = []
	file_list.append(commit_hash)
	for file in files:
		if file[1] == "production":
			continue
		file_list.append(file[0])
	csvWriter.writerow(file_list)
	f.close()
	return

def csv_writer(pjt_name, commit_hash, date, author, files):
	f_pc = open(pjt_name + '.csv', 'a')
	csvWriter_pc = csv.writer(f_pc, lineterminator="\n")
	size = os.path.getsize(pjt_name + '.csv')
	if size == 0:
		title = ["Date", "Commit_hash", "Author", "File", "Attribution"]
		csvWriter_pc.writerow(title)
	f_all = open(pjt_name + '_all.csv', 'a')
	csvWriter_all = csv.writer(f_all, lineterminator="\n")
	size = os.path.getsize(pjt_name + '_all.csv')
	if size == 0:
		title = ["Date", "Commit_hash", "Author", "File", "Attribution"]
		csvWriter_all.writerow(title)
	for file in files:
		file_list = []
		file_list.append(commit_hash)
		file_list.append(date)
		file_list.append(author)
		file_list.append(file[0])
		file_list.append(file[1])
		if file[1] == "test":
			csvWriter_all.writerow(file_list)
			continue
		csvWriter_pc.writerow(file_list)
		csvWriter_all.writerow(file_list)
	f_pc.close()
	f_all.close()
	return

def log_scraper(pjt_name):
	f = open("log_"+pjt_name+".txt", 'r')
	line = f.readline()
	tc_count = 0
	while line:
		#while not line.startswith("author:"):
		while line == "\n":
			line = f.readline()
			if not line:
				break
		if line.startswith("commit:"):
			commit_hash = line.split("commit:")[-1]
			commit_hash = commit_hash.replace("\n", "")
			line = f.readline()
		if line.startswith("author:"):
			author = line.split("author:")[-1]
			author = author.replace("\n", "")
			line = f.readline()
		if line.startswith("date:"):
			utime = line.split("date:")[-1]
			utime = utime.replace("\n", "")
			date = str(datetime.datetime.fromtimestamp(int(utime)))
			date = date.split(" ")[0]
			date = date.replace("-", "/")
			line = f.readline()
		file_list = []
		while (not line == "\n") and (line):
			#file_path = line.replace("\n", "")
			#file_name = file_path.split("/")[-1]
			file_name = line.replace("\n", "")
			if file_name.endswith("Test.java") or file_name.endswith("Tests.java"):
				file_attribution = "test"
			elif file_name.endswith(".java"):
				file_attribution = "production"
			else:
				line = f.readline()
				continue
			file_info = []
			file_info.append(file_name)
			file_info.append(file_attribution)
			file_list.append(file_info)
			line = f.readline()
		if len(file_list) > 0:
			csv_writer(pjt_name, commit_hash, date, author, file_list)
			for file_info in file_list:
				if file_info[1] == "test":
					csv_writer_tc(pjt_name, commit_hash, file_list)
					tc_count += 1
					break
		line = f.readline()
	f.close()
	print str(tc_count) + " commits contain TC modification."
	return

if __name__ == "__main__":
	argvs = sys.argv
	pjt_name = argvs[1]
	log_scraper(pjt_name)
