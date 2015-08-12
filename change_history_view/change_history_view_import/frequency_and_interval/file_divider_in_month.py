# -*- coding: utf-8 -*-
"""
integrate (pjt_name).csv and file_id_list.csv and create change_history_view.csv

input: (pjt_name).csv
	   file_id_list.csv
output: change_history_view.csv
"""
import os
import csv
import sys

month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
year_list = ["2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015"]

for year in year_list:
	files = []
	for month in month_list:
		query = '"^' + year + '/' + month + '/"'
		file_name = 'chv_' + year + '_' + month + '.csv'
		cmd = 'grep ' + query + ' chv_for_commit_interval_checking.csv > ' + file_name
		os.system(cmd)
		files.append(file_name)
		if month == "06" or month == "12":
			query = " ".join(files)
			if month == "06":
				cmd = 'cat ' + query + ' > chv_' + year + '_01_06.csv'
			else:
				cmd = 'cat ' + query + ' > chv_' + year + '_07_12.csv'
			os.system(cmd)
			for file_name in files:
				cmd = 'rm ' + file_name
				os.system(cmd)
			files = []
