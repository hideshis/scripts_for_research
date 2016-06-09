# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import csv
from base_method import base_method

class caller_method:
    def __init__(self, method_info):
        self.caller_method_info = base_method(method_info[-3])
        self.caller_method_info.java_name = method_info[0]
        self.caller_method_info.begin_line = int(method_info[-2])
        self.caller_method_info.end_line = int(method_info[-1])
        self.outbound_dependency_list = []
        return

    def get_outbound_dependency(self):
        self.get_outbound_dependency = []
        return

    def get_callee_method(self):
        return
