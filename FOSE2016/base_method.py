# -*- coding: utf-8 -*-
import sys
import subprocess
import os
import csv

class base_method:
    def __init__(self, method_name):
        self.method_name = method_name
        self.begin_line = 0
        self.end_line = 0
        self.buggy = False
        self.covered = False

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
        self.covered = False
        return
