# -*- coding: utf-8 -*-
"""
This script parses index.html files created by Jacoco and obtain test coverage for each file.
"""
import subprocess
import sys
import os
import urllib2
import lxml.html
import csv
from lxml import etree

f_write = open('coverage_info_by_file_level.csv', 'w')
csvWriter = csv.writer(f_write, lineterminator='\n')
header = ['project', 'num_covered_instruction', 'num_uncovered_instruction', 'num_total_instruction', 'C0coverage']
csvWriter.writerow(header)
f_read = open('coverage_info.csv', 'r')
dataReader = csv.reader(f_read)
row = dataReader.next()
pjt_id = row[0]
coverage_of_pjt = row[-1].replace('\r','').replace('\n','')
pjt_name = pjt_id.split('/')[-1]
pjt_path = '/Users/kenjiro/Desktop/hideshi-s/msrmc2017/' + pjt_name
#pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/' + pjt_name
loc_list = []
uncovered_loc_list = []
while pjt_name:
	print pjt_name
	if coverage_of_pjt == 'N/A':
		row = dataReader.next()
		pjt_id = row[0]
		coverage_of_pjt = row[-1].replace('\r','').replace('\n','')
		pjt_name = pjt_id.split('/')[-1]
		pjt_path = '/Users/kenjiro/Desktop/hideshi-s/msrmc2017/' + pjt_name
		#pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/' + pjt_name
		continue
	try:
		result = subprocess.check_output('find ' + pjt_path + ' | grep "/target/site/jacoco/" | grep "\.html$" | grep -v "\.java\.html$" | grep -v "index\.html$" | grep -v "index\.source\.html$" | grep -v "jacoco-sessions\.html" | grep -v "\.sessions\.html"', shell=True)
		coverage_report_existence_flag = True
	except subprocess.CalledProcessError:
		coverage_report_existence_flag = False
	if coverage_report_existence_flag == True:
		result = result.replace('\r', '')
		result_list = result.split('\n')
		result_list.pop()
		#for html_path in result_list:
		#	print html_path
		for html_path in result_list:
			print html_path
			root = lxml.html.parse(html_path).getroot()
			for tr_counter in range(1, len(root.xpath("/html/body/table/tbody/tr"))+1):
				C0coverage = root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[3]")[0].text.replace('%','')
				print C0coverage
				if C0coverage == '0':
					num_covered_instruction = 0
					try:
						num_uncovered_instruction = int(root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[2]/img")[0].attrib['alt'].replace(',',''))
					except IndexError:
						num_uncovered_instruction = 'N/A'
					num_total_instruction = num_uncovered_instruction
				elif C0coverage == '100':
					try:
						num_covered_instruction = int(root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[2]/img")[0].attrib['alt'].replace(',',''))
					except IndexError:
						num_covered_instruction = 'N/A'
					num_total_instruction = num_covered_instruction
					num_uncovered_instruction = 0
				else:
					for img_counter in range(1,3):
						try:
							if "greenbar.gif" in root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[2]/img["+str(img_counter)+"]")[0].attrib['src']:
								num_covered_instruction = int(root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[2]/img["+str(img_counter)+"]")[0].attrib['alt'].replace(',',''))
							else:
								num_uncovered_instruction = int(root.xpath("/html/body/table/tbody/tr[" + str(tr_counter) + "]/td[2]/img["+str(img_counter)+"]")[0].attrib['alt'].replace(',',''))
						except IndexError:
							num_covered_instruction = 'N/A'
							num_uncovered_instruction = 'N/A'
							break
					if num_covered_instruction == 'N/A':
						num_total_instruction = 'N/A'
					else:
						num_total_instruction = str(int(num_covered_instruction) + int(num_uncovered_instruction))
				print num_covered_instruction, num_uncovered_instruction, num_total_instruction
				coverage_info = []
				coverage_info.append(pjt_id)
				coverage_info.append(num_covered_instruction)
				coverage_info.append(num_uncovered_instruction)
				coverage_info.append(num_total_instruction)
				coverage_info.append(C0coverage)
				csvWriter.writerow(coverage_info)
	else:
		coverage_info = []
		coverage_info.append(pjt_id)
		coverage_info.append('N/A')
		coverage_info.append('N/A')
		coverage_info.append('N/A')
		coverage_info.append('N/A')
		csvWriter.writerow(coverage_info)
	row = dataReader.next()
	pjt_id = row[0]
	coverage_of_pjt = row[-1].replace('\r','').replace('\n','')
	pjt_name = pjt_id.split('/')[-1]
	pjt_path = '/Users/kenjiro/Desktop/hideshi-s/msrmc2017/' + pjt_name
	#pjt_path = '/Users/hideshi-s/Desktop/msrmc2017/' + pjt_name
f_write.close()
f_read.close()
