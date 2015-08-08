# -*- coding: utf-8 -*-
"""
this script gives for each product codes.

input:  pc_without_tc_without_bug.csv
        pc_without_tc_with_bug.csv
        pc_with_tc_without_bug.csv
        pc_with_tc_with_bug.csv
output: files_pc_without_tc_without_bug.csv
        files_pc_without_tc_with_bug.csv
        files_pc_with_tc_without_bug.csv
        files_pc_with_tc_with_bug.csv
        file_id_list_pc_without_tc_without_bug.csv
        file_id_list_pc_without_tc_with_bug.csv
        file_id_list_pc_with_tc_without_bug.csv
        file_id_list_pc_with_tc_with_bug.csv
"""

import re
import sys
import csv
import os.path
import os
import subprocess
import csv

def id_giver_production(id_max, read_file_name, write_file_name):
	id = id_max
	writer = csv.writer(file(write_file_name, "w"), lineterminator="\n")
	f = open(read_file_name, 'r')
	line = f.readline()
	while line:
		file_info = []
		file_info.append(line.replace("\n", ""))
		file_info.append(id)
		writer.writerow(file_info)
		line = f.readline()
		id += 1
	f.close()
	return id

def file_id_giver(pjt_name):
    id_max = 1
    command = "cat pc_without_tc_without_bug.csv | cut -d',' -f3 | sort | uniq > files_pc_without_tc_without_bug.txt"
    subprocess.call(command, shell=True)
    id_max = id_giver_production(id_max, "files_pc_without_tc_without_bug.txt", "file_id_list_pc_without_tc_without_bug.csv")

    command = "cat pc_without_tc_with_bug.csv | cut -d',' -f3 | sort | uniq > files_pc_without_tc_with_bug.txt"
    subprocess.call(command, shell=True)
    id_max = id_giver_production(id_max, "files_pc_without_tc_with_bug.txt", "file_id_list_pc_without_tc_with_bug.csv")

    command = "cat pc_with_tc_without_bug.csv | cut -d',' -f3 | sort | uniq > files_pc_with_tc_without_bug.txt"
    subprocess.call(command, shell=True)
    id_max = id_giver_production(id_max, "files_pc_with_tc_without_bug.txt", "file_id_list_pc_with_tc_without_bug.csv")

    command = "cat pc_with_tc_with_bug.csv | cut -d',' -f3 | sort | uniq > files_pc_with_tc_with_bug.txt"
    subprocess.call(command, shell=True)
    id_max = id_giver_production(id_max, "files_pc_with_tc_with_bug.txt", "file_id_list_pc_with_tc_with_bug.csv")
    return

if __name__ == "__main__":
	argvs = sys.argv
	pjt_name = argvs[1]
	file_id_giver(pjt_name)
