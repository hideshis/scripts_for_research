# -*- coding: utf-8 -*-

import sys
import time
import csv
import os
import sonarqube_scraper

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
    cmd = 'mvn clean org.jacoco:jacoco-maven-plugin:prepare-agent install -Dmaven.test.failure.ignore=true'
    os.system(cmd)
    cmd = 'mvn sonar:sonar'
    os.system(cmd)
    os.chdir("..")
    time.sleep(60)
    sonarqube_scraper.func(commit_date)
    line = f.readline()
    line = line.replace("\n", "")
f.close()
