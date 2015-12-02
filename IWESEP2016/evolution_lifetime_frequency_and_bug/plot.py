# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import csv
import numpy
import matplotlib.pyplot as plt

def plotter(result, title):
    result = result.replace('\r', '')
    result_list = result.split('\n')
    result_list.pop()
    data_list = []
    for x in result_list:
        data_list.append(float(x))
    data = numpy.array(data_list)
    plt.hold(False)
    plt.hist(data)
    plt.savefig(title + ".png")
    return

result = subprocess.check_output('cat synthesized_info.csv | sed -n 2,\$p | cut -d"," -f2', shell=True)
plotter(result, "co_evolution")
result = subprocess.check_output('cat synthesized_info.csv | sed -n 2,\$p | cut -d"," -f4', shell=True)
plotter(result, "commit_frequency")
result = subprocess.check_output('cat synthesized_info.csv | sed -n 2,\$p | cut -d"," -f3', shell=True)
plotter(result, "lifetime")
