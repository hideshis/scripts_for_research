#!/bin/bash

rm -rf ./nones/
mkdir ./nones
rm none.csv
grep 'none,none' java_class_method_link.csv > none.csv
ARRAY=(`cat none.csv | cut -d"," -f2`)
for file_name in ${ARRAY[@]};
do
    #echo $file_name
    cp $file_name ./nones
done;
