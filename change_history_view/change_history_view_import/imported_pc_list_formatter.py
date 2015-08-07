# -*- coding: utf-8 -*-
"""
this script formats imported_pc_list.csv

input: imported_pc_list.csv
output: imported_pc_list_formatted.csv
"""

import sys
import os
import subprocess
import csv

def getDirList():
    dir_list = []
    file_dir_list = os.listdir("./")
    for file_dir in file_dir_list:
        if os.path.isdir(file_dir):
            dir_list.append(file_dir)
    return dir_list

def formatter(directory, file_name):
    os.chdir("./" + directory)
    f = open("imported_pc_list.csv", "r")
    writer = csv.writer(file("imported_pc_list_formatted.csv", "w"), lineterminator="\n")
    dataReader = csv.reader(f)
    commit_hash_check = ""
    first_flag = 0
    for row in dataReader:
        commit_hash = row[0]
        pc = row[1]
        if commit_hash == commit_hash_check:
            pc_list.append(pc)
        else:
            if first_flag == 0:
                first_flag = 1
                commit_hash_check = commit_hash
                pc_list = []
                pc_list.append(pc)
                continue
            pc_text = ":".join(pc_list)
            import_info = []
            import_info.append(commit_hash_check)
            import_info.append(pc_text)
            writer.writerow(import_info)
            commit_hash_check = commit_hash
            pc_list = []
            pc_list.append(pc)
    pc_text = ":".join(pc_list)
    import_info = []
    import_info.append(commit_hash_check)
    import_info.append(pc_text)
    writer.writerow(import_info)
    os.chdir("..")
    return

if __name__ == "__main__":
    argvs = sys.argv
    pjt_name = argvs[1]
    dir_list = getDirList()
    print dir_list
    for directory in dir_list:
        if not directory.startswith("process"):
            continue
        print directory +  " started."
        file_name = 'imported_pc_list_' + directory + '.csv'
        formatter(directory, file_name)
        print directory +  " have been finished."
