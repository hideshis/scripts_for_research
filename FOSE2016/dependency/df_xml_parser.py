# -*- coding: utf-8 -*-
from xml.etree import ElementTree
import sys
import csv
import subprocess
import os

def name_conversion(target):
    if target == None:
        return 'no_name'
    else:
        try:
            target_name = target[:target.index("(")] # hoge(foo.var.fuga, piyo) -> hoge
            target_parameter = target[target.index("(")+1:-1] # hoge(foo.var.fuga, piyo) -> foo.var.fuga, piyo
            if target_parameter != '()':
                target_parameter_list = []
                for param in target_parameter.split(','): # foo.var.fuga, piyo -> [fuga, piyo]
                    param = param.replace(' ', '')
                    param = param.split('.')[-1]
                    param = param.split('$')[-1]
                    target_parameter_list.append(param)
                    target_name = target_name + '(' + ','.join(target_parameter_list) + ')'
                    return target_name
            else:
                return target_name + '()'
        except ValueError:
            return target


argvs = sys.argv
xml_file = argvs[1]
output_file = argvs[2]
f = open(output_file, 'w')
csvWriter = csv.writer(f, lineterminator='\n', delimiter='|')
tree = ElementTree.parse(xml_file)
root = tree.getroot()
for e_package in root.findall('package'):
    e_package_name = e_package.find('name').text
    if e_package_name == None:
        e_package_name = 'no_name_package'
    #print e_package_name
    for e_class in e_package.findall('class'):
        e_class_name = e_class.find('name').text
        if e_class_name == None:
            e_class_name = 'no_class_name'
        #print e_package_name + ',' + e_class_name
        for e_feature in e_class.findall('feature'):
            #tmp = e_feature.find('name').text
            e_feature_name = name_conversion(e_feature.find('name').text)
            """
            if tmp == None:
                e_feature_name = 'no_feature_name'
            else:
                try:
                    e_feature_name = tmp[:tmp.index("(")] # hoge(foo.var.fuga, piyo) -> hoge
                    e_feature_parameter = tmp[tmp.index("(")+1:-1] # hoge(foo.var.fuga, piyo) -> foo.var.fuga, piyo
                    if e_feature_parameter != '()':
                        e_feature_parameter_list = []
                        for param in e_feature_parameter.split(','): # foo.var.fuga, piyo -> [fuga, piyo]
                            param = param.replace(' ', '')
                            param = param.split('.')[-1]
                            param = param.split('$')[-1]
                            e_feature_parameter_list.append(param)
                        e_feature_name = e_feature_name + '(' + ','.join(e_feature_parameter_list) + ')'
                    else:
                        e_feature_name = e_feature_name + '()'
                except ValueError:
                    e_feature_name = tmp
                """
            outbound_list = []
            for outbound in e_feature.findall('outbound'):
                outbound_list.append(name_conversion(outbound.text))
            #os.system('echo "' + str(len(outbound_list)) + '">>hogehoge.txt')
            if len(outbound_list) == 0:
                info = [e_package_name, e_class_name, e_feature_name, ""]
                csvWriter.writerow(info)
            else:
                for outbound in outbound_list:
                    info = [e_package_name, e_class_name, e_feature_name, outbound]
                    csvWriter.writerow(info)
f.close()
