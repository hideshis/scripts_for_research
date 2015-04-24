# -*- coding: utf-8 -*-
import re
import csv
import os.path
import os
import sys
import time

pjt_name = sys.argv[1]
file_name_authors = pjt_name + "_authors.csv"
file_name_issue_report = pjt_name + "_issue_reports.csv"
f_authors = opne(file_name_authors, "r")
line_author = f_authors.readline() # header line
line_author = f_authors.readline()
while line:
	author_name = line_author.split(",")[0]
	print author_name
	egrep_query = "   \",\"" + author_name + "   \",\""
	os.system("egrep " + egrep_query + " " + file_name_issue_report)
	time.sleep(2)
	line_author = f_authors.readline()