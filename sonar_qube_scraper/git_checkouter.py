# -*- coding: utf-8 -*-
"""
git log --date=short --pretty=format:"%ad %h" > commit_date_hash_list.txt
"""


import sys
import time
import csv
import os
import sonarqube_scraper
import subprocess

def sub_system_name_getter(commit_date):
    writer = csv.writer(file('sub_system_name_list_' + commit_date + '.csv', 'w'), lineterminator="\n")
    header = ["sub_system_name_sonar", "sub_system_name_dir"]
    writer.writerow(header)
    dir_list = os.listdir("./")
    for directory in dir_list:
        if os.path.isdir(directory):
            os.chdir("./" + directory + "/")
            file_list = os.listdir("./")
            if "pom.xml" in file_list:
                cmd = 'grep "<name>" pom.xml'
                result = subprocess.check_output(cmd, shell=True)
                sub_system_name_sonar = result.split(">")[1]
                sub_system_name_sonar = sub_system_name_sonar.split("<")[0]
                sub_system_name_dir = directory
                sub_system_info = []
                sub_system_info.append(sub_system_name_sonar)
                sub_system_info.append(sub_system_name_dir)
                writer.writerow(sub_system_info)
            os.chdir("..")
    cmd = 'mv sub_system_name_list_' + commit_date + '.csv ..'
    os.system(cmd)

argvs = sys.argv
pjt_name = argvs[1]
f = open("git_checkout_list.txt", "r")
line = f.readline()
line = line.replace("\n", "")
while line:
    commit_date = line.split(" ")[0]
    commit_hash = line.split(" ")[1]
    os.chdir("./" + pjt_name)
    cmd = 'git checkout ' + commit_hash
    os.system(cmd)
    sub_system_name_getter(commit_date)
    cmd = 'mvn clean org.jacoco:jacoco-maven-plugin:0.7.4.201502262128:prepare-agent install -Dmaven.test.failure.ignore=true --fail-never'
    os.system(cmd)
    cmd = 'mvn sonar:sonar'
    os.system(cmd)
    os.chdir("..")
    time.sleep(10)
    sonarqube_scraper.func(commit_date)
    line = f.readline()
    line = line.replace("\n", "")
    sys.exit("execution abortion")
f.close()
