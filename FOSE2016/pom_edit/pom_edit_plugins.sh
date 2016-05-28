#!/bin/bash

pom=$1
lineNo=$2
flag=$3
script_array1_1=("<build>" "<plugins>")
script_array1_2=("</plugins>" "</build>")
script_array2_1=("<plugins>")
script_array2_2=("</plugins>")
script_array3=("<plugin>" "<artifactId>maven-surefire-plugin</artifactId><version>2.18.1</version>" "<configuration>")
script_array4=("<disableXmlReport>true</disableXmlReport>" "<systemPropertyVariables>" "<coverage-output>html</coverage-output>")
script_array5=("<coverage-outputDir>\${project.build.directory}/coverage-report</coverage-outputDir>" "<coverage-maxCallPoints>10000</coverage-maxCallPoints>")
script_array6=("</systemPropertyVariables>" "</configuration>" "</plugin>")
if [ "$flag" = "no_build" ];
then
	script_array=(${script_array1_1[*]} ${script_array3[*]} ${script_array4[*]} ${script_array5[*]} ${script_array6[*]} ${script_array1_2[*]})
elif [ "$flag" = "build_but_no_plugins" ]
then
	script_array=(${script_array2_1[*]} ${script_array3[*]} ${script_array4[*]} ${script_array5[*]} ${script_array6[*]} ${script_array2_2[*]})
else
	script_array=(${script_array3[*]} ${script_array4[*]} ${script_array5[*]} ${script_array6[*]})
fi
./pom_writer.sh ${pom} ${lineNo} ${script_array[@]}
