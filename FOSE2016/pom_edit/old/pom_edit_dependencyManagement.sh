#!/bin/bash

pom=$1
result=`grep -n '</dependencyManagement>' $1`
if [ -n "$result" ];
then
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	let lineNo-=1
	script_array1=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "<version>\${jmockit.version}</version>" "<scope>test</scope>" "</dependency>")
	script_array2=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit-coverage</artifactId>" "<version>\${jmockit.version}</version>" "<scope>runtime</scope>" "<optional>true</optional>" "</dependency>")
	script_array=(${script_array1[*]} ${script_array2[*]})
	./pom_writer.sh ${pom} ${lineNo} ${script_array[@]}
else
	result=`grep -n '</project>' $1`
	arr=(`echo $result | tr -s ':' ' '`)
	lineNo=${arr[0]}
	script_array1=("<dependencyManagement>" "<dependencies>")
	script_array2=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "<version>\${jmockit.version}</version>" "<scope>test</scope>" "</dependency>")
	script_array3=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit-coverage</artifactId>" "<version>\${jmockit.version}</version>" "<scope>runtime</scope>" "<optional>true</optional>" "</dependency>")
	script_array4=("</dependencies>" "</dependencyManagement>")
	script_array=(${script_array1[*]} ${script_array2[*]} ${script_array3[*]} ${script_array4[*]})
	./pom_writer.sh ${pom} ${lineNo} ${script_array[@]}
fi
