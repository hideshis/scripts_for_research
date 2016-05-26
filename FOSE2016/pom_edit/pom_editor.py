# -*- coding: utf-8 -*-
import subprocess
import sys
import os

def dependencies_end_lineNo_getter(pom):
    try:
        result = subprocess.check_output('grep -n "</dependencyManagement>" ' + pom, shell=True)
        dM_lineNo = result.split(':')[0]
        result = subprocess.check_output('grep -n "</dependencies>" ' + pom, shell=True)
        result_list = result.split('\n')
        result_list.pop()
        print result_list
        if len(result_list) == 1: # <dependencyManagement>直下にのみ，<dependencies>が存在している
            result = subprocess.check_output('grep -n "</project>" ' + pon, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return dependencies_lineNo
        elif len(result_list) == 2: # <dependencyManagement>直下以外にも，<dependencies>が存在している
            for var in result_list:
                dependencies_lineNo = var.split(':')[0]
                if (int(dependencies_lineNo)+1) == int(dM_lineNo):
                    continue
                else:
                    return dependencies_lineNo
        else:
            print 'there are three or more "</dependencies>" tags.'
            sys.exit()
    except subprocess.CalledProcessError:
        try:
            result = subprocess.check_output('grep -n "</dependencies>" ' + pom, shell=True)
            result_list = result.split('\n')
            result_list.pop()
            # <dependencies>がpom.xmlにある場合
            if len(result_list) == 1:
                return result.split(':')[0]
            else:
                print 'there are two or more "</dependencies>" tags while there is not "</dependencyManagement>" tag.'
                sys.exit()
        except subprocess.CalledProcessError: # <dependencies>がpom.xmlにない場合
            result = subprocess.check_output('grep -n "</project>" ' + pon, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return dependencies_lineNo
    print 'some error has occurred.'
    sys.exit()

def dependencies_begin_lineNo_getter(pom):
    try:
        result = subprocess.check_output('grep -n "<dependencyManagement>" ' + pom, shell=True)
        dM_lineNo = result.split(':')[0]
        result = subprocess.check_output('grep -n "<dependencies>" ' + pom, shell=True)
        result_list = result.split('\n')
        result_list.pop()
        print result_list
        if len(result_list) == 1: # <dependencyManagement>直下にのみ，<dependencies>が存在している
            result = subprocess.check_output('grep -n "</project>" ' + pon, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return dependencies_lineNo
        elif len(result_list) == 2: # <dependencyManagement>直下以外にも，<dependencies>が存在している
            for var in result_list:
                dependencies_lineNo = var.split(':')[0]
                if (int(dependencies_lineNo)-1) == int(dM_lineNo):
                    continue
                else:
                    return str(int(dependencies_lineNo)+1)
        else:
            print 'there are three or more "<dependencies>" tags.'
            sys.exit()
    except subprocess.CalledProcessError:
        try:
            result = subprocess.check_output('grep -n "<dependencies>" ' + pom, shell=True)
            result_list = result.split('\n')
            result_list.pop()
            # <dependencies>がpom.xmlにある場合
            if len(result_list) == 1:
                return str(int(result.split(':')[0])+1)
            else:
                print 'there are two or more "<dependencies>" tags while there is not "<dependencyManagement>" tag.'
                sys.exit()
        except subprocess.CalledProcessError: # <dependencies>がpom.xmlにない場合
            result = subprocess.check_output('grep -n "</project>" ' + pon, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return dependencies_lineNo
    print 'some error has occurred.'
    sys.exit()

def pom_edit(pom):
    os.system('./pom_edit_properties.sh ' + pom)
    os.system('./pom_edit_dependencyManagement.sh ' + pom)
    dependencies_begin_lineNo = dependencies_begin_lineNo_getter(pom)
    print dependencies_begin_lineNo
    dependencies_end_lineNo = dependencies_end_lineNo_getter(pom)
    print dependencies_end_lineNo
    return

pjt_path = '/Users/hideshi-s/Desktop/httpclient'
print pjt_path
result = subprocess.check_output('find ' + pjt_path, shell=True)
result = result.replace('\r', '')
pom_candidate_list = result.split('\n')
pom_list = [pom_candidate for pom_candidate in pom_candidate_list if pom_candidate.endswith('pom.xml')]
print '\n'.join(pom_list)
for pom in pom_list:
    if pom == pjt_path + '/pom.xml':
        continue
    pom_edit(pom)
    sys.exit()
