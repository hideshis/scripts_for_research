# -*- coding: utf-8 -*-
import sys
import subprocess
from caller_method import caller_method
from base_method import base_method

if __name__ == "__main__":
    f = open('./file_class_method_link/file_class_method_converted.csv', 'r')
    for line in f.readlines():
        caller = caller_method(line.replace('\r', '').replace('\n', '').split('|'))
        print caller.caller_method_info.java_name
        print caller.caller_method_info.method_name
        print caller.caller_method_info.begin_line, caller.caller_method_info.end_line
        caller.caller_method_info.is_covered()
        #sys.exit()
