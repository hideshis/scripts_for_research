#!/bin/bash

function insert {
	pom=$1
	lineNo=$2
	script=$3
	gsed """${lineNo}i ${script}""" $pom > ./pom.xml
	mv ./pom.xml $pom
}


pom=$1
lineNo=$2
shift 2
script_array=($@)
flag=0
for script in ${script_array[@]}
do
	if [ $flag = 0 ];
	then
		let flag+=1
	else
		let lineNo+=1
	fi
	insert ${pom} ${lineNo} ${script}
done
let lineNo+=1
