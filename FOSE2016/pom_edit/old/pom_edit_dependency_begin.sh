#!/bin/bash

pom=$1
lineNo=$2
flag=$3
if [ $flag = "yes" ];
then
	script_array=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "</dependency>")
else
	script_array=("<dependencies>" "<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit</artifactId>" "</dependency>" "</dependencies>")
fi
./pom_writer.sh ${pom} ${lineNo} ${script_array[@]}
