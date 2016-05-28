# -*- coding: utf-8 -*-
import subprocess
import sys
import os

def hoge(pom):
    try:
        result = subprocess.check_output('grep -n "<build>" ' + pom, shell=True)
        build_begin_lineNo = int(result.split(':')[0]) # <build> exists in pom.xml
        result = subprocess.check_output('grep -n "</build>" ' + pom, shell=True)
        build_end_lineNo = int(result.split(':')[0])
        try:
            result = subprocess.check_output('grep -n "<plugins>" ' + pom, shell=True)
            plugins_lineNo_list = [var.split(':')[0] for var in result.split('\n') if var != ""]
            for plugins_lineNo in plugins_lineNo_list:
                if (build_begin_lineNo < int(plugins_lineNo)) and (int(plugins_lineNo) < build_end_lineNo):
                    return 'build and plugins', str(int(plugins_lineNo)+1) # <plugins> exists between <build> and </build>
            return 'build but no plugins', str(build_end_lineNo) # <plugins> does not exist between <build> and </build>
        except subprocess.CalledProcessError: # <plugins> does not exist in pom.xml
            return 'build but no plugins', str(build_end_lineNo) # <plugins> does not exist between <build> and </build>
    except subprocess.CalledProcessError: # <build> does not exist in pom.xml
        result = subprocess.check_output('grep -n "</project>" ' + pom, shell=True)
        plugins_lineNo = result.split(':')[0]
        return 'no build', plugins_lineNo

def dependencies_end_lineNo_getter(pom):
    try:
        result = subprocess.check_output('grep -n "</dependencyManagement>" ' + pom, shell=True)
        dM_lineNo = result.split(':')[0]
        result = subprocess.check_output('grep -n "</dependencies>" ' + pom, shell=True)
        result_list = result.split('\n')
        result_list.pop()
        print result_list
        if len(result_list) == 1: # <dependencyManagement>直下にのみ，<dependencies>が存在している
            result = subprocess.check_output('grep -n "</project>" ' + pom, shell=True)
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
            result = subprocess.check_output('grep -n "</project>" ' + pom, shell=True)
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
            result = subprocess.check_output('grep -n "</project>" ' + pom, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return 'dependencies does not exist', dependencies_lineNo
        elif len(result_list) == 2: # <dependencyManagement>直下以外にも，<dependencies>が存在している
            for var in result_list:
                dependencies_lineNo = var.split(':')[0]
                if (int(dependencies_lineNo)-1) == int(dM_lineNo):
                    continue
                else:
                    return 'dependencies exists', str(int(dependencies_lineNo)+1)
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
                return 'dependencies exists', str(int(result.split(':')[0])+1)
            else:
                print 'there are two or more "<dependencies>" tags while there is not "<dependencyManagement>" tag.'
                sys.exit()
        except subprocess.CalledProcessError: # <dependencies>がpom.xmlにない場合
            result = subprocess.check_output('grep -n "</project>" ' + pom, shell=True)
            dependencies_lineNo = result.split(':')[0]
            return 'dependencies does not exist', dependencies_lineNo
    print 'some error has occurred.'
    sys.exit()

def pom_edit(pom):
    os.system('./pom_edit_properties.sh ' + pom)
    os.system('./pom_edit_dependencyManagement.sh ' + pom)
    msg, dependencies_begin_lineNo = dependencies_begin_lineNo_getter(pom)
    print dependencies_begin_lineNo
    if msg == 'dependencies exists':
        param_list = [pom, dependencies_begin_lineNo, 'yes']
    else:
        param_list = [pom, dependencies_begin_lineNo, 'no']
    os.system('./pom_edit_dependency_begin.sh ' + ' '.join(param_list))
    dependencies_end_lineNo = dependencies_end_lineNo_getter(pom)
    print dependencies_end_lineNo
    param_list = [pom, dependencies_end_lineNo]
    os.system('./pom_edit_dependency_end.sh ' + ' '.join(param_list))
    msg, plugins_lineNo = hoge(pom)
    print plugins_lineNo
    if msg == 'build and plugins':
        param_list = [pom, plugins_lineNo, 'build_and_plugins']
    elif msg == 'build but no plugins':
        param_list = [pom, plugins_lineNo, 'build_but_no_plugins']
    else:
        param_list = [pom, plugins_lineNo, 'no_build']
    os.system('./pom_edit_plugins.sh ' + ' '.join(param_list))
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
