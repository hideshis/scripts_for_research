# -*- coding: utf-8 -*-
import re
import csv
import os.path
import os


def csv_writer(filename, date, author, files):
	f = open(filename + '.csv', 'a')
	csvWriter = csv.writer(f, lineterminator="\n")
	size = os.path.getsize(filename + '.csv')
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

def log_scraper(filename):
	f = open("log_"+filename+".txt", 'r')
	line = f.readline()
	while line:
		if line.startswith("commit "):	# コミット
			line = f.readline()
		if line.startswith("Merge: "):	# マージ
			line = f.readline()
		if line.startswith("Author: "):	# 開発者名
			author = line.split(' ')[-1]
			author = author.replace("\n", "")
			#print author
			line = f.readline()
		if line.startswith("Date: "):	# 変更日
			tmp = (line.split('   ')[-1]).split('-')
			date = tmp[0] + tmp[1] + tmp[2]
			date = date.replace("\n", "")
			#print date
			line = f.readline()
			line = f.readline()
			if not line:
				break
		while line != "\n":	# コメント
			line = f.readline()
			if not line:
				break
		line = f.readline()
		if not line:
			break
		elif line.startswith("commit "):
			continue
		files = []
		while (line != "\n") and line:	# 変更されたファイル一覧
			line = line.replace("\n", "")
			### view描画用の変更：ここから ###
			if line.startswith("src/main/"):
                                line = line.split("/")[-1]
                                files.append(line)
			if line.startswith("src/tests") or line.startswith("src/testcases"):
                                line = line.split("/")[-1]
                                files.append(line)
			### view描画用の変更：ここまで ###
			#files.append(line)
			line = f.readline()
		#for file in files:
			#print file
		if len(files) > 0:
        		csv_writer(filename, date, author, files)
		if line:
        		line = f.readline()
		
log_scraper("ant")
