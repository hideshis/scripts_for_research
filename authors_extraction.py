# -*- coding: utf-8 -*-
"""
This script extract authors.
file(s) required:
	log_(project name).txt
data structrue required:
	./(project name)/log_(project name1).txt
file(s) created:
	./(project name)/(project name)_authors.txt
Usage:
	python authors_extraction.py (project name)
notes:
	the authors' role is expressed as a value ranging from 0 to 1.
	0 means that the author is pure-tester.
	1 means that the author is pure-product developer.
	the value is calculated based on the # of times that the developer modified the test code and product code.
	shown below is the exuasion to calculate the value:
		(authors' role) = (# of times of pc modification) / ((# of times of pc modification)+(# of times of tc modification))
		where pc and tc mean product code and test code, respectively.
	for example, assuming that the author modified test code twice and product code once. then the value is
		(author's role) = 1 / (1 + 2) = 0.333...
	the value means that the author is a tester rather than product developer.
"""

import re
import csv
import os.path
import os
import sys
import commands
import time

# extract authors from the commit log
def authors_name_extraction(pjt_name):
	f = open("log_" + pjt_name + ".txt", "r")
	f_write = open(pjt_name + '_authors.csv', 'w')
	csvWriter = csv.writer(f_write, lineterminator="\n")
	title = ["author_name", "author_address"]
	csvWriter.writerow(title)
	line = f.readline() # delete header
	author_list = [] # authors who have already been added to the (pjt_name)_authors.txt
	while line:
		while not line.startswith("Author: "):
			line = f.readline()
			if not line:
				f.close()
				f_write.close()
				return
		line = line.replace("\n", "")
		line = line[8:]
		mail_address_start_point = line.rfind("<")
		author_name = line[:mail_address_start_point]
		author_name = author_name[:-1] # eliminate a space
		"""
		author_mail_address = line[mail_address_start_point:]
		author_mail_address = author_mail_address.replace("<", "")
		author_mail_address = author_mail_address.replace(">", "")
		"""
		#author_role = author_role_identification(pjt_name, author_name) # identify the author's role
		author_info = []
		author_info.append(author_name)
		#author_info.append(author_mail_address)
		"""
		author_info.append(author_role["test"])
		author_info.append(author_role["product"])
		author_info.append(author_role["role"])
		"""
		# check if the author has already been added to the (pjt_name)_authors.txt
		if not author_info in author_list:
			author_list.append(author_info)
			print author_info
			csvWriter.writerow(author_info)
		line = f.readline()
	xf.close()
	f_write.close()
	return

# identify whether the author is a pure-tester, a pure-product developer,
# or a developer who wrote both test and product code
def authors_role_extraction(pjt_name):
	author_list_file_name = pjt_name + "_authors.csv"
	result_file_name = pjt_name + "_authors_with_roles.csv"
	f_write = open(result_file_name, "w")
	csvWriter = csv.writer(f_write, lineterminator="\n")
	title = ["author_name", "num_of_test_modification", "num_of_product_modification", "author_role"]
	csvWriter.writerow(title)
	pjt_file_name = pjt_name + ".csv"
	tmp_file_name1 = "tmp1.csv"
	tmp_file_name2 = "tmp2.csv"
	f_author_list = open(author_list_file_name, "r")
	line_author_list = f_author_list.readline() # header of the file
	line_author_list = f_author_list.readline()
	loc = sum(1 for line in open(author_list_file_name))
	loc -= 1 # sbutract header
	print loc
	finish_counter = 0
	while line_author_list:
		line_author_list = line_author_list.replace("\n", "")
		author_name = line_author_list.split(",")[0]
		author_name = author_name.replace("(", "\(")
		author_name = author_name.replace(")", "\)")
		egrep_query = "^[0-9]{8}," + author_name + ","
		os.system("egrep \"" + egrep_query + "\" " + pjt_file_name + " > " + tmp_file_name1) # extract all files commited by the author
		os.system("cut -d ',' -f 7 " + tmp_file_name1 + " > " + tmp_file_name2) # eliminate redundant info.
		file_size = os.path.getsize(tmp_file_name2)
		if file_size == 0:
			print "author " + author_name + " has not wrote any codes"
			time.sleep(3)
		# count how much the author have commited test coded and product codes
		else:
			role_dict = {"test":0, "product":0}
			f_tmp = open(tmp_file_name2, "r")
			line_tmp = f_tmp.readline()
			while line_tmp:
				line_tmp = line_tmp.replace("\n", "")
				if line_tmp == "test":
					role_dict["test"] += 1
				elif line_tmp == "product":
					role_dict["product"] += 1
				else:
					sys.exit("file type error: the commited file's type is neither test nor product")
				line_tmp = f_tmp.readline()
			f_tmp.close()
			author_role = {"test":0, "product":0, "role":0}
			author_role["test"] = role_dict["test"]
			author_role["product"] = role_dict["product"]
			try:
				author_role["role"] = float(author_role["product"])/float(author_role["test"] + author_role["product"])
			except ZeroDivisionError:
				sys.exit("file count errror: the author didn't commited neither test nor product code")
			author_info = []
			author_info.append(line_author_list.split(",")[0])
			#author_info.append(line_author_list.split(",")[1])
			author_info.append(author_role["test"])
			author_info.append(author_role["product"])
			author_info.append(author_role["role"])
			csvWriter.writerow(author_info)
		line_author_list = f_author_list.readline()
		finish_counter += 1
		print "role extraction: " + str(finish_counter) + "/" + str(loc) + " have been finished"
	f_author_list.close()
	f_write.close()
	os.system("rm " + tmp_file_name1)
	os.system("rm " + tmp_file_name2)
	os.system("mv " + result_file_name + " " + author_list_file_name)
	return

pjt_name = sys.argv[1]
print pjt_name
authors_name_extraction(pjt_name)
authors_role_extraction(pjt_name)