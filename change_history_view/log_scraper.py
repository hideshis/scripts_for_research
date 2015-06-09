# -*- coding: utf-8 -*-
"""
the log file is extracted by the following command:
	git log --pretty=format:"%nauthor:%an %ndate:%at" --name-only > log_(project_name).txt
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
		title = ["Date", "Author", "File"]
		csvWriter.writerow(title)
	for file in files:
		file_list = []
		file_list.append(date)
		file_list.append(author)
		file_list.append(file)
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
			line = f.readline()
		file_list = []
		while (not line == "\n") and (line):
			file_list.append(line.replace("\n", ""))
			line = f.readline()
		if len(file_list) > 0:
			print pjt_name, date, author, str(file_list)
        	csv_writer(pjt_name, date, author, file_list)
		line = f.readline()

log_scraper("eclipse_jdt")
