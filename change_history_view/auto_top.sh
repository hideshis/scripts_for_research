#!/bin/sh
project_dir_name="ant_data"
project_file="ant.csv"
revision_file="revision_ant.csv"
link_integrated_file="linkdata_integrated.csv"
link_file="link.csv"
integrated_file="info.csv"
chmod 777 ${project_dir_name}
rm ${project_dir_name}
chmod 777 ${project_file}
rm ${project_file}
chmod 777 ${revision_file}
rm ${revision_file}
mkdir ${project_dir_name}
python log_scraper.py
python revision_hash_getter.py
python checkouter_ant.py
cp ${project_file} ${project_dir_name}
cp csv_integrater_hoge.py ${project_dir_name}
cd ${project_dir_name}
cat "linkdata"*.csv > ${link_integrated_file}
sort -t , -u ${link_integrated_file} > ${link_file}
python csv_integrater_hoge.py ${project_file} ${link_file} ${integrated_file}
cd ..