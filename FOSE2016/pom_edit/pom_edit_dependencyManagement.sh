#!/bin/bash

function insert {
	pom=$1
	lineNo=$2
	script=$3
	gsed """${lineNo}i ${script}""" $pom > ./pom.xml
	mv ./pom.xml $pom
}

function script_for {
	pom=$1
	lineNo=$2
	shift 2
	script_array=($@)
	#script_array=(`echo $script`)
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
	return
}

pom=$1
result=`grep -n '</dependencyManagement>' $1`
if [ -n "$result" ];
then
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	let lineNo-=1
	echo $lineNo
	script_array1=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "<version>\${jmockit.version}</version>" "<scope>test</scope>" "</dependency>")
	script_array2=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit-coverage</artifactId>" "<version>\${jmockit.version}</version>" "<scope>runtime</scope>" "<optional>true</optional>" "</dependency>")
	script_array=(${script_array1[*]} ${script_array2[*]})
	script_for ${pom} ${lineNo} ${script_array[@]}
else
	result=`grep -n '</project>' $1`
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	script_array1=("<dependencyManagement>" "<dependencies>")
	script_array2=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "<version>\${jmockit.version}</version>" "<scope>test</scope>" "</dependency>")
	script_array3=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit-coverage</artifactId>" "<version>\${jmockit.version}</version>" "<scope>runtime</scope>" "<optional>true</optional>" "</dependency>")
	script_array4=("</dependencies>" "</dependencyManagement>")
	script_array=(${script_array1[*]} ${script_array2[*]} ${script_array3[*]} ${script_array4[*]})
	script_for ${pom} ${lineNo} ${script_array[@]}
fi
#result=`grep -n '</dependencyManagement>' $1`
