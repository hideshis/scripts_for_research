# -*- coding: utf-8 -*-
#from lxml import etree
import lxml.html as lh
import os
import sys
import csv

pre_class_list = []
prettyprint_covered_counter = 0
prettyprint_covered_list = []
branch_list = []

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
    global pre_class_list
    global prettyprint_covered_counter
    global prettyprint_covered_list
    global branch_list
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
                if (td.find('pre') != None):
                    pre_class_list.append(td.find('pre').attrib['class'])
                    #if td.find('pre').attrib['class'] == 'prettyprint covered':
                    if td.find('pre').attrib['class'] == 'prettyprint covered':
                        prettyprint_covered_list.append(file_name_original+','+lineNo)
                        prettyprint_covered_counter += 1
                if (td.find('pre') != None) and (td.find('pre').attrib['class'] == 'prettyprint covered cp'):
                    ol = td.find('ol')
                    cover_list.append(lineNo)
                    cover_list.append('fully covered')
                    # Each of lis contains name of test case.
                    for li in ol:
                        cover_list.append(li.text.replace(': ', '#'))
                elif (td.find('pre') != None) and (td.find('pre').attrib['class'] == 'prettyprint jmp'):
                    span_list = td.find('pre')
                    ol_list = td.findall('ol')
                    if len(span_list) == len(ol_list):
                        covered_flag = 0
                        for span, ol in zip(span_list, ol_list):
                            if span.attrib['class'] == 'covered cp':
                                covered_flag = 1
                                if len(cover_list) == 0:
                                    cover_list.append(lineNo)
                                    cover_list_child = []
                                    status_flag = 'fully covered'
                                for li in list(ol):
                                    cover_list_child.append(li.text.replace(': ', '#'))
                            else:
                                status_flag = 'partially covered'
                        if covered_flag == 1:
                            cover_list_child = list(set(cover_list_child))
                            cover_list.append(status_flag)
                            cover_list.extend(cover_list_child)
                    else:
                        print len(span_list), len(ol_list)
                        sys.exit()
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
        print file_name_original
        print file_path, file_name
        directory_creator(file_path, file_name)
        html_convertor(file_path, file_name, file_name_original)
global pre_class_list
global prettyprint_covered_counter
global prettyprint_covered_list
for hoge in list(set(pre_class_list)):
    print hoge
print '# of prettyprint covered: ' + str(prettyprint_covered_counter)
for hoge in prettyprint_covered_list:
    print hoge
