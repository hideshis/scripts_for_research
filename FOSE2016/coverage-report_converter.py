# -*- coding: utf-8 -*-
#from lxml import etree
import lxml.html as lh
import os
import sys
import csv

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

os.system('rm -rf ./coverage-report_formatted')
os.system('mkdir coverage-report_formatted')
for file_name in fild_all_files('./coverage-report'):
    if file_name.endswith('.html') and (file_name != './coverage-report/index.html'):
        print file_name
        file_name_output = file_name[2:]
        file_name_output = file_name_output.replace('/', '_')
        file_name_output = file_name_output.replace('.html', '.csv')
        f_write = open('./coverage-report_formatted/'+file_name_output, 'w')
        csvWriter = csv.writer(f_write, lineterminator='\n')
        f = open(file_name, 'r')
        root = lh.fromstring(f.read().decode('utf-8'))
        tr_list = root.xpath('/html/body/table/tr')
        for tr in tr_list:
            cover_list = []
            for td in tr:
                try:
                    if td.attrib['class'] == 'line':
                        #print 'line No.: ' + str(td.text)
                        lineNo = str(td.text)
                except KeyError:
                    if (td.find('pre') != None) and (td.find('pre').attrib['class'] == 'prettyprint covered cp'):
                        ol = td.find('ol')
                        cover_list.append(lineNo)
                        for li in ol:
                            #print li.text
                            cover_list.append(li.text.replace(': ', '#'))
            if len(cover_list) > 0:
                csvWriter.writerow(cover_list)
                print ','.join(cover_list)
                print '---'
        f.close()
        f_write.close()
