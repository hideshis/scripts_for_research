#!/bin/bash
cat bug_location_info.csv | cut -d',' -f4 | sort | uniq > buggy_commit_list.csv
