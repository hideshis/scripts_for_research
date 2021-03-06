# Execution Procedure:
1. ./jira/jira_report_analyzer.py
  - This script collects JIRA's issue reports.
1. ./szz_tag/tag_info_formatter.py
  - This script identifies time-stamp of each releases.
1. ./post_release_bug/post_release_bug_getter.py
  - This script divides bugs into pre-release-bugs, post-release_bugs, and others.
1. ./bug_location/bug_location_getter.py
  - This script identifies file, lines, and revision of each bugs.
1. ./bug_location/buggy_commit_list_getter.sh
  - This script lists up commits which induced bug(s).
1. ./file_class_method_link/JPsample.jar
  - Usage: java -jar JPsample.jar (full path of the directory which you want to analyze) (full path of the file which you want to output the result)
  - Example: java -jar JPsample.jar /Users/hideshi-s/Desktop/httpclient/httpclient5/src/main/java/ /Users/hideshi-s/Desktop/scripts_for_research/FOSE2016/file_class_method_link/
  - This script lists classes and methods of each Java files. It also identifies start line and end line of each classes and methods.
1. ./dependency/df_xml_parser.py
  - This script formats the result of DependencyFinder.
1. ./coverage_report/coverage-report_converter.py
  - This script converts original JMockit coverage report (.html file) into .csv file.
1. ./pom_edit/pom_editor_new.py
