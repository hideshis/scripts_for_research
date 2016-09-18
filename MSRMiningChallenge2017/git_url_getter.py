# -*- coding: utf-8 -*-
import os

f = open('maven_projects.csv', 'r')
pjt_id = f.readline().replace('\r', '').replace('\n', '')
pjt_name = pjt_id.split('/')[-1]
while pjt_id:
    git_url = 'https://github.com/' + pjt_id + '.git'
    print git_url
    os.system('git clone ' + git_url)
    os.chdir('./pom_edit/jacoco')
    os.system('python pom_editor_exe.py ' + pjt_name)
    os.chdir('../..')
    os.chdir('./' + pjt_name)
    os.system('mvn clean test jacoco:report -fn')
    os.chdir('..')
    pjt_id = f.readline().replace('\r', '').replace('\n', '')
    pjt_name = pjt_id.split('/')[-1]
f.close()
