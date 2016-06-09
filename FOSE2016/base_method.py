# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import csv

class base_method:
    def __init__(self, method_name):
        self.java_name = ''
        self.method_name = method_name
        self.begin_line = 0
        self.end_line = 0
        self.buggy = False
        self.covered = False

    @property
    def java_name(self):
        return self.java_name

    @java_name.setter
    def java_name(self, java_name):
        self.java_name = java_name
        return

    @property
    def begin_line(self):
        return self.begin_line

    @begin_line.setter
    def begin_line(self, begin_line):
        self.begin_line = begin_line
        return

    @property
    def end_line(self):
        return self.end_line

    @end_line.setter
    def end_line(self, end_line):
        self.end_line = end_line
        return

    def is_buggy(self):
        self.buggy = False
        return

    def is_covered(self):
        result = subprocess.check_output('find ./coverage_report/coverage-report_converted/ -name ' + self.java_name.split('/')[-1].replace('.java', '.csv'), shell=True)
        result = result.replace('\r', '')
        result_list = result.split('\n')
        result_list.pop()
        coverage_report_name = ''
        for coverage_report_candidate in result_list:
            if self.java_name.replace('.java', '.csv') in coverage_report_candidate:
                coverage_report_name = coverage_report_candidate
                break
        if coverage_report_name == '':
            self.covered = False
        else:
            for line_num in range(self.begin_line, self.end_line+1):
                print line_num
                try:
                    result = subprocess.check_output('grep "$' + str(line_num) + '|" ' + coverage_report_name, shell=True)
                    self.covered = True
                    break
                except subprocess.CalledProcessError:
                    self.covered = False
                    continue
        return
