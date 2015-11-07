# -*- coding: utf-8 -*-
"""
this script extract commit hash and modified files from commit log.
they are exracted only if the commit message contain designated keywords.
the log file is extracted by the following command:
	git log --pretty=format:"__commit_hash__:%n%h%n__commit_message__:%n%B%n__modified_files__:" --name-only > log_httpclient_minami.txt

usage:
python commit_message_scraper.py (keyword1) (keyword2) (keyword3) ...

input: log_httpclient_minami.txt
output: result.csv
"""
import re
import sys
import csv
import os.path
import os
import datetime

def keyword_checker(keyword_list):
	f = open("log_httpclient_minami.txt", "r")
	writer = csv.writer(file('result.csv', 'w'), lineterminator="\n")
	line = f.readline()
	line = line.replace("\r", "")
	line = line.replace("\n", "")
	while line:
		if line.startswith("__commit_hash__"): # commit hash part
			line = f.readline()
			line = line.replace("\r", "")
			line = line.replace("\n", "")
			commit_hash = line
			line = f.readline()
		else:
			sys.exit("error at parsing commit hash")

		if line.startswith("__commit_message__"): # commit message part
			line = f.readline()
			commit_message = ""
			while not line.startswith("__modified_files__"):
				line = line.replace("\r", "")
				line = line.replace("\n", " ")
				commit_message += line
				line = f.readline()
		else:
			sys.exit("error at parsing commit message")

		if line.startswith("__modified_files__"):  # modified files part
			line = f.readline()
			modified_files = ""
			while (not line.startswith("__commit_hash__")) and line:
				line = line.replace("\r", "")
				line = line.replace("\n", "")
				if not line == "":
					if modified_files == "":
						modified_files = line
					else:
						modified_files += "|" +  line
				line = f.readline()
		else:
			sys.exit("error at parsing modified files")

		for keyword in keyword_list:
			if keyword in commit_message:
				info_list = []
				info_list.append(commit_hash)
				info_list.append(modified_files)
				writer.writerow(info_list)
				break
		line = line.replace("\r", "")
		line = line.replace("\n", "")
	f.close()

argvs = sys.argv
keyword_list = argvs
keyword_checker(keyword_list)
