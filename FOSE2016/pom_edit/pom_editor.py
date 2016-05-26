# -*- coding: utf-8 -*-
import subprocess
import sys
import os

def pom_edit(pom):
    os.system('./pom_edit1.sh ' + pom)
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
