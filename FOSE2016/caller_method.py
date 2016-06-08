# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import csv

class caller_method:
    def __init__(self, method_info):
        self.method_name = method_info[-3]
        self.begin_line = int(method_info[-2])
        self.end_line = int(method_info[-1])