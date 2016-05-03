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

def directory_creator(file_path, file_name):
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    return

def html_convertor(file_path, file_name, file_name_original):
    file_name_output = file_name.replace('.html', '.csv')
    f_write = open(file_path + '/' + file_name_output, 'w')
    csvWriter = csv.writer(f_write, lineterminator='\n')
    f = open(file_name_original, 'r')
    root = lh.fromstring(f.read().decode('utf-8'))
    tr_list = root.xpath('/html/body/table/tr')
    # one tr equals to one line of code
    for tr in tr_list:
        cover_list = []
        # Each of tds contains detail information of one line of code
        for td in tr:
            try:
                # get line number
                if td.attrib['class'] == 'line':
                    lineNo = str(td.text)
            except KeyError:
                # get test cases which tests the line of code
                if (td.find('pre') != None) and (td.find('pre').attrib['class'] == 'prettyprint covered cp'):
                    ol = td.find('ol')
                    cover_list.append(lineNo)
                    # Each of lis contains name of test case.
                    for li in ol:
                        cover_list.append(li.text.replace(': ', '#'))
        # if len(cover_list) > 0 is True, it means that one or more test cases
        # cover the line of code.
        if len(cover_list) > 0:
            csvWriter.writerow(cover_list)
            print ','.join(cover_list)
            print '---'
    f.close()
    f_write.close()
    return

def file_name_and_path_getter(file_name):
    file_name = file_name[2:]
    file_name = file_name.replace('/target/coverage-report/', '/')
    path_list = file_name.split('/')
    file_name = path_list.pop(-1)
    file_path = './coverage-report_converted/' + '/'.join(path_list)
    return file_path, file_name

os.system('rm -rf ./coverage-report_converted')
for file_name in fild_all_files('./'):
    if ('/coverage-report/' in file_name) and file_name.endswith('.html') and (not file_name.endswith('/coverage-report/index.html')):
        file_name_original = file_name
        file_path, file_name = file_name_and_path_getter(file_name)
        print file_path, file_name
        directory_creator(file_path, file_name)
        html_convertor(file_path, file_name, file_name_original)
