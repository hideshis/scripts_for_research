#!/bin/bash

pom=$1
lineNo=$2
script_array=("<dependency>" "<groupId>org.jmockit</groupId><artifactId>jmockit-coverage</artifactId>" "</dependency>")
./pom_writer.sh ${pom} ${lineNo} ${script_array[@]}
