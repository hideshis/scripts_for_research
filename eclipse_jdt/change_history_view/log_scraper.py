# -*- coding: utf-8 -*-
"""
this script extracts commit info.
the commits are memorized only if one ore more java files are commited.
the log file is extracted by the following command:
	git log --pretty=format:"%nauthor:%an%ndate:%at" --name-only > log_(project_name).txt
this script is called by auto_top.sh

input: log_(project_name).txt
output: (project_name).csv
"""
import re
import sys
import csv
import os.path
import os
import datetime

def csv_writer(pjt_name, date, author, files):
	f = open(pjt_name + '.csv', 'a')
	csvWriter = csv.writer(f, lineterminator="\n")
	size = os.path.getsize(pjt_name + '.csv')
	if size == 0:
		title = ["Date", "Author", "File", "Attribution"]
		csvWriter.writerow(title)
	for file in files:
		file_list = []
		file_list.append(date)
		file_list.append(author)
		file_list.append(file[0])
		file_list.append(file[1])
		csvWriter.writerow(file_list)
	f.close()
	return

def log_scraper(pjt_name):
	f = open("log_"+pjt_name+".txt", 'r')
	line = f.readline()
	while line:
		while not line.startswith("author:"):
			line = f.readline()
			if not line:
				break
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
			file_path = line.replace("\n", "")
			file_name = file_path.split("/")[-1]
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
			csv_writer(pjt_name, date, author, file_list)
		line = f.readline()
	f.close()
	return

if __name__ == "__main__":
	log_scraper("eclipse_jdt")
