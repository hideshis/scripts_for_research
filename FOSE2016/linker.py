# -*- coding: utf-8 -*-
import sys
import subprocess
import caller_method

if __name__ == "__main__":
    f = open('./file_class_method_link/file_class_method_converted.csv', 'r')
    for line in f.readlines():
        caller = caller_method.caller_method(line.replace('\r', '').replace('\n', '').split('|'))
        print caller.method_name
        sys.exit()
