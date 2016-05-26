#!/bin/bash

function insert {
	pom=$1
	lineNo=$2
	script=$3
	gsed """${lineNo}i ${script}""" $pom > ./pom.xml
	mv ./pom.xml $pom
}

pom=$1
result=`grep -n '</properties>' $1`
if [ -n "$result" ];
then
	echo $result
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	insert $pom $lineNo "<jmockit.version>1.23</jmockit.version>"
else
	result=`grep -n '</project>' $1`
	echo $result
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	flag=0
	script_array=("<properties>" "<jmockit.version>1.23</jmockit.version>" "</properties>")
	for script in ${script_array[@]}
	do
		if [ $flag = 0 ];
		then
			let flag+=1
		else
			let lineNo+=1
		fi
		insert $pom $lineNo $script
	done
fi
#result=`grep -n '</dependencyManagement>' $1`
