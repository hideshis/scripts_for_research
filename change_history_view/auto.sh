#!/bin/sh
all_code_path="C:/Users/hideshi/git/ant/src"
#all_code_files="files_ant.txt"
#all_code_files=$1
#product_code_path="C:/Users/hideshi/git/ant/src/main/java"
#product_code_files="files_main_ant.txt"
product_code_files=$1
#test_code_path="C:/Users/hideshi/git/ant/src/test/java"
#test_code_files="files_test_ant.txt"
test_code_files=$2
#link_file="linkdata.csv"
link_file=$3
project_file="ant.csv"
integrated_file="integrated.csv"
dir_name=$4
revision_file="revision_ant.csv"
project_dir_name="ant_data"
python file_finder.py ${all_code_path} ${product_code_files} ${test_code_files}
python files_integrator.py ${product_code_files} ${test_code_files} ${link_file}
mkdir ${dir_name}
mv ${product_code_files} ${dir_name}
mv ${test_code_files} ${dir_name}
cp ${link_file} ${project_dir_name}
mv ${link_file} ${dir_name}
mv ${dir_name} ${project_dir_name}
#python csv_integrater_hoge.py ${project_file} ${link_file} ${integrated_file}
