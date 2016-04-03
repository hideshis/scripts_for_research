# -*- coding: utf-8 -*-
"""
this script identifies testing product codes for each test codes.
this is done by analyzing import statement.
if a test code imports product codes, then this script interpretes that
the test code tests these product codes.

input: (pjt_name)_tc.csv
       target project's git repository
output: imported_pc_list.csv
        files_list.txt
"""

import sys
import os
import subprocess
import csv

# check out the target git repository
def check_outer(pjt_name, commit_hash):
    os.chdir("./" + pjt_name)
    cmd = 'git checkout ' + commit_hash
    os.system(cmd)
    os.chdir("../")

def recursive_search(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

# create the file list of the target repository
def find_all_files(pjt_name):
    os.chdir("./" + pjt_name)
    f = open("file_list.txt", "w")
    for file in recursive_search('./'):
        file = file.replace("\\", "/")
        file = file[2:]
        if file.endswith(".java"):
            f.write(file + "\n")
    f.close()
    cmd = 'mv file_list.txt ../'
    os.system(cmd)
    os.chdir("../")

def file_finder_by_naming_convention(tc):
    if tc.startswith("src/"):
        query = tc.replace('src/test/', 'src/java/')
    else:
        query = tc.replace('/src/test/', '/src/main/')
    try:
        result = subprocess.check_output('grep "' + query + '" file_list.txt', shell=True)
        result = result.replace("\r", "")
        imported_file_list = result.split("\n")
        imported_file_list.pop()
        return imported_file_list
    except subprocess.CalledProcessError:
        return ['none']

def file_finder(tc, imported_file_candidate_list):
    path_head = tc.split("/test/")[0] + "/main/java/"
    imported_file_list = []
    for target in imported_file_candidate_list:
        if " static " in target:
            target = target.split("static ")[-1]
            path_list = target.split(".")
            path_list.pop() # remove method name
            target = "/".join(path_list)
        else:
            target = target.split("import ")[-1]
            target = target.replace(".", "/")
        #target = "/" + target + ".java"
        target = path_head + target + ".java"
        cmd = 'grep "' + target + '" file_list.txt'
        try:
            result = subprocess.check_output(cmd, shell=True)
            file_list = result.split("\n")
            file_list.pop() # remove blank factor
            imported_file_list.extend(file_list)
        except subprocess.CalledProcessError: # when the importing pc doesn't exist in the file_list.txt
            file_list = []
    return imported_file_list

def importing_pc_identifier(pjt_name, commit_hash, tc_list):
    writer = csv.writer(file("imported_pc_list.csv", "a"), lineterminator="\n")
    for tc in tc_list:
        cmd = 'grep "^import" ./' + pjt_name + '/' + tc
        imported_file_list = []
        try:
            imported_file_by_name = file_finder_by_naming_convention(tc)
            if not imported_file_by_name[0] != "none":
                imported_file_list.extend(imported_file_by_name)
            result = subprocess.check_output(cmd, shell=True)
            result = result.replace("\r", "")
            imported_file_candidate_list = result.split(";\n")
            imported_file_candidate_list.pop() # remove blank factor
            imported_file_list.extend(file_finder(tc, imported_file_candidate_list))
            if len(imported_file_list) == 0:
                cmd = 'echo ' + tc + '>> no_importing_tc_list.txt'
                os.system(cmd)
                cmd = 'cat no_importing_tc_list.txt | sort | uniq > tmp.txt'
                os.system(cmd)
                cmd = 'mv tmp.txt no_importing_tc_list.txt'
                os.system(cmd)
            else:
                for imported_file in imported_file_list:
                    info_list = []
                    info_list.append(commit_hash)
                    info_list.append(imported_file)
                    writer.writerow(info_list)
        except subprocess.CalledProcessError: # if the tc doesn't import any pcs
            if len(imported_file_list) == 0:
                print "no imports"
            else:
                for imported_file in imported_file_list:
                    info_list = []
                    info_list.append(commit_hash)
                    info_list.append(imported_file)
                    writer.writerow(info_list)


if __name__ == "__main__":
    argvs = sys.argv
    pjt_name = argvs[1]
    f = open(pjt_name + "_tc.csv")
    line = f.readline()
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    end_counter = 0
    while line:
        factors = line.split(",")
        commit_hash = factors[0]
        tc_list = factors[1:]
        check_outer(pjt_name, commit_hash)
        find_all_files(pjt_name)
        importing_pc_identifier(pjt_name, commit_hash, tc_list)
        os.system("rm file_list.txt")
        line = f.readline()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        end_counter += 1
        print str(end_counter) + " have been finished."
