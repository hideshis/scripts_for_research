# -*- coding: utf-8 -*-
"""
this script extracts commited date and its hashu number.
the log file is extracted by the following command:
	git log --pretty=format:"%nrevision:%h%nauthor:%an%ndate:%at" --name-only > log_(project_name).txt
this script is called by auto_top.sh

input: log_(project_name).txt
output: revision_(project_name).csv
"""
import re
import sys
import csv
import os.path
import os
import datetime

def csv_writer(pjt_name, date, revision):
	f = open('revision_' + pjt_name + '.csv', 'a')
	csvWriter = csv.writer(f, lineterminator="\n")
	size = os.path.getsize('revision_' + pjt_name + '.csv')
	if size == 0:
		title = ["Date", "Revision"]
		csvWriter.writerow(title)
	file_list = []
	file_list.append(date)
	file_list.append(revision)
	csvWriter.writerow(file_list)
	f.close()
	return

def log_scraper(pjt_name):
	f = open("log_"+pjt_name+".txt", 'r')
	line = f.readline()
	while line:
		while not line.startswith("revision:"):
			line = f.readline()
			if not line:
				break
		if line.startswith("revision:"):
			revision = line.split("revision:")[-1]
			revision = revision.replace("\n", "")
			line = f.readline()
		if line.startswith("author:"):
			line = f.readline()
		if line.startswith("date:"):
			utime = line.split("date:")[-1]
			utime = utime.replace("\n", "")
			date = str(datetime.datetime.fromtimestamp(int(utime)))
			date = date.split(" ")[0]
			line = f.readline()
		file_list = []
		while (not line == "\n") and (line):
			file_list.append(line.replace("\n", ""))
			line = f.readline()
		if len(file_list) > 0:
			csv_writer(pjt_name, date, revision)
		line = f.readline()


log_scraper("eclipse_jdt")
