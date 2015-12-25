# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import csv

f = open("synthesized_info.csv", "r")
lines = f.readlines()
flag = 0
for line in lines:
    if flag == 0: # remove header
        flag = 1
        continue
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    factor = line.split(",")
    co_evo = factor[1]
    lifetime = factor[2]
    interval = factor[3]
    if float(lifetime) > 869:
        if float(interval) > 31.0:
            if float(co_evo) > 0.100:
                os.system('echo ' + line + '>>llt_li_hr.csv')
            else:
                os.system('echo ' + line + '>>llt_li_lr.csv')
        else:
            if float(co_evo) > 0.100:
                os.system('echo ' + line + '>>llt_si_hr.csv')
            else:
                os.system('echo ' + line + '>>llt_si_lr.csv')
    else:
        if float(interval) > 31.0:
            if float(co_evo) > 0.100:
                os.system('echo ' + line + '>>slt_li_hr.csv')
            else:
                os.system('echo ' + line + '>>slt_li_lr.csv')
        else:
            if float(co_evo) > 0.100:
                os.system('echo ' + line + '>>slt_si_hr.csv')
            else:
                os.system('echo ' + line + '>>slt_si_lr.csv')
f.close()

"""
os.system("sed -n '2,$p' synthesized_info.csv | sort -g -t , -k2,2 | head -n 173 > lr.csv")
os.system("sed -n '2,$p' synthesized_info.csv | sort -g -t , -k2,2 | tail -n 173 > hr.csv")

os.system("cat hr.csv | sort -g -t , -k3,3 | head -n 86 > hr_slt.csv")
os.system("cat hr.csv | sort -g -t , -k3,3 | tail -n 87 > hr_llt.csv")
os.system("cat lr.csv | sort -g -t , -k3,3 | head -n 86 > lr_slt.csv")
os.system("cat lr.csv | sort -g -t , -k3,3 | tail -n 87 > lr_llt.csv")

os.system("cat hr_llt.csv | sort -g -t , -k4,4 | head -n 44 > hr_llt_mf.csv")
os.system("cat hr_llt.csv | sort -g -t , -k4,4 | tail -n 43 > hr_llt_lf.csv")
os.system("cat hr_slt.csv | sort -g -t , -k4,4 | head -n 43 > hr_slt_mf.csv")
os.system("cat hr_slt.csv | sort -g -t , -k4,4 | tail -n 43 > hr_slt_lf.csv")
os.system("cat lr_llt.csv | sort -g -t , -k4,4 | head -n 44 > lr_llt_mf.csv")
os.system("cat lr_llt.csv | sort -g -t , -k4,4 | tail -n 43 > lr_llt_lf.csv")
os.system("cat lr_slt.csv | sort -g -t , -k4,4 | head -n 43 > lr_slt_mf.csv")
os.system("cat lr_slt.csv | sort -g -t , -k4,4 | tail -n 43 > lr_slt_lf.csv")
"""
