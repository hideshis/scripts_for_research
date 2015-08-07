# -*- coding: utf-8 -*-
"""
integrate imported_pc_list_formatted.csv and (pjt_name).csv and update (pjt_name).csv.
input: imported_pc_list_formatted.csv
       (pjt_name).csv
output: (pjt_name).csv
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

def file_mover(directory, file_name):
    os.chdir("./" + directory)
    #cmd = 'cp imported_pc_list_formatted.csv ' + file_name
    #os.system(cmd)
    cmd = 'cp ' + file_name + ' ..'
    os.system(cmd)
    os.chdir("..")

def integrator(pjt_name, directory, file_name):
    f = open(file_name, "r")
    line = f.readline()
    line = line.replace("\n", "")
    finish_counter = 0
    while line:
        commit_hash = line.split(",")[0]
        linked_pc = line.split(",")[1]
        linked_pc_list = linked_pc.split(":")
        # obtain commit info
        cmd = 'grep "' + commit_hash + '" ' + pjt_name + '_all.csv'
        result = subprocess.check_output(cmd, shell=True)
        commit_info = result.split("\n")[0]
        commit_info_list = commit_info.split(",")
        # integrate commit info
        writer = csv.writer(file(pjt_name+'.csv', "a"), lineterminator="\n")
        for linked_pc in linked_pc_list:
            linked_pc_commit_info_list = []
            linked_pc_commit_info_list.append(commit_info_list[0])
            linked_pc_commit_info_list.append(commit_info_list[1])
            linked_pc_commit_info_list.append(commit_info_list[2])
            linked_pc_commit_info_list.append(linked_pc)
            linked_pc_commit_info_list.append("test")
            writer.writerow(linked_pc_commit_info_list)
        line = f.readline()
        line = line.replace("\n", "")
        finish_counter += 1
        print directory + " " + str(finish_counter)
    return

if __name__ == "__main__":
    argvs = sys.argv
    pjt_name = argvs[1]
    dir_list = getDirList()
    print dir_list
    for directory in dir_list:
        if not directory.startswith("process"):
            continue
        file_name = 'imported_pc_list_formatted.csv'
        file_mover(directory, file_name)
        integrator(pjt_name, directory, file_name)
        cmd = 'rm imported_pc_list_formatted.csv'
        os.system(cmd)
        print directory +  " have been finished."
