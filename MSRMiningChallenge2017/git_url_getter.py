# -*- coding: utf-8 -*-
import os

f = open('maven_projects.csv', 'r')
pjt_name = f.readline().replace('\r', '').replace('\n', '')
while pjt_name:
    git_url = 'https://github.com/' + pjt_name + '.git'
    print git_url
    #os.system('git clone ' + git_url)
    pjt_name = f.readline().replace('\r', '').replace('\n', '')
f.close()
