# -*- coding: utf-8 -*-
"""
This script parses a projects' log.
To execute this script, you should prepare files listed below:
log_(project name).txt
The txt file should be created by a command shown below:
"git log --date=short --numstat > log_(project name).txt"

After the execution, a file shown below is created:
(project name).csv
(project name)_comments.csv
"Comment_d" in "(project name).csv" and "comment_id" in  "(project name)" are corresponding.
So you can trace the comment posted at a change of a file.

Usage: python log_scraper (project name)

***caution***
all commas (",") in each message are replaced with "__hogeHOGE__".
I did this because the file created by this script is .csv file and
each information is splitted by commas.
***caution***
"""

import re
import csv
import os.path
import os
import sys
comment_id = 1

def csv_writer(filename, date, author, files, comment, commit):
	global comment_id
	f = open(filename + '.csv', 'a')
	csvWriter = csv.writer(f, lineterminator="\n")
	size = os.path.getsize(filename + '.csv')
	if size == 0:
		title = ["Date", "Author", "File", "added", "deleted", "churn", "sort", "comment_id", "commit"]
		csvWriter.writerow(title)
	for file in files:
		file_list = []
		file_list.append(date)
		file_list.append(author)
		file_list.append(file[2])
		file_list.append(file[0])
		file_list.append(file[1])
		file_list.append(str(int(file[0])+int(file[1])))
		file_list.append(file[-1])
		file_list.append(comment_id)
		file_list.append(commit)
		csvWriter.writerow(file_list)
	f.close()
	f_comment = open(filename + "_comments.csv", "a")
	csvWriter = csv.writer(f_comment, lineterminator="\n")
	size = os.path.getsize(filename + '_comments.csv')
	if size == 0:
		title = ["comment_id", "comment"]
		csvWriter.writerow(title)
	comment_list = []
	comment_list.append(comment_id)
	comment_list.append(comment)
	csvWriter.writerow(comment_list)
	f_comment.close()
	comment_id += 1
	return

def log_scraper(filename):
	f = open("log_"+filename+".txt", 'r')
	line = f.readline()
	finish_counter = 1
	while line:
		# one loop parses one commit
		if line.startswith("commit "):	# commit
			line = line.replace("\n", "")
			commit = line.split(" ")[1]
			line = f.readline()
		if line.startswith("Merge: "):	# merge
			line = f.readline()
		if line.startswith("Author: "):	# committer name
			"""
			author = line.split(' ')[-1]
			author = author.replace("\n", "")
			"""
			line = line.replace("\n", "")
			line = line[8:]
			mail_address_start_point = line.rfind("<")
			author_name = line[:mail_address_start_point]
			author_name = author_name[:-1] # eliminate a space
			author_mail_address = line[mail_address_start_point:]
			author_mail_address = author_mail_address.replace("<", "")
			author_mail_address = author_mail_address.replace(">", "")
			line = f.readline()
		if line.startswith("Date: "):	# commit date
			tmp = (line.split('   ')[-1]).split('-')
			date = tmp[0] + tmp[1] + tmp[2]
			date = date.replace("\n", "")
			line = f.readline()
			line = f.readline()
			if not line:
				break
		comment = ""
		# comment
		while line.startswith("    "):
			line = line.replace(",", "__hogeHOGE__")
			comment = comment + line.replace("\n", "")
			line = f.readline()
			if not line:
				print str(finish_counter) + "th commit is parsed"
				break
		line = f.readline()
		if not line:    # if true, reading all log is finished
			break
		elif line.startswith("commit "):
			print str(finish_counter) + "th commit is parsed"
			finish_counter += 1
			continue
		files = []
		while (line != "\n") and line:	# files which are modified in the commit
			line = line.replace("\n", "")
			line_list = line.split('\t')
			path_list = line_list[2].split("/")
			"""
			if (len(path_list) >= 2) and (path_list[0].endswith(".java")): # filter only .java files
                                if "test" in "/".join(path_list): # identify if the file is a test code
                                        line_list.append("test")
                                else:
                                        line_list.append("product")
                                if line_list[0] == "-":
                                        line_list[0] = "0"
                                if line_list[1] == "-":
                                        line_list[1] = "0"
				line_list[2] = line_list[2].replace(",", "__hogeHOGE__")
                                files.append(line_list)
			"""
                        if "test" in "/".join(path_list): # identify if the file is a test code
                                line_list.append("test")
                        else:
                                line_list.append("product")
                        if line_list[0] == "-":
                                line_list[0] = "0"
                        if line_list[1] == "-":
                                line_list[1] = "0"
			line_list[2] = line_list[2].replace(",", "__hogeHOGE__")
                        files.append(line_list)
			line = f.readline()
		if len(files) > 0: # record to .csv file only if .java files are modifiled in the commit
			"""
        	author = author.replace("<", "")
               	author = author.replace(".", "")
                       author = author.replace("@", "")
        	author = author.replace(" ", "")
               	author = author.replace(">", "")
            """
        	csv_writer(filename, date, author_name, files, comment, commit)
		if line:
        		line = f.readline()
		print str(finish_counter) + "th commit is parsed"
		finish_counter += 1
argvs = sys.argv
log_scraper(argvs[1])