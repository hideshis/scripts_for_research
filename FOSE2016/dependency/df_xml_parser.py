from xml.etree import ElementTree
import sys
import csv

XMLFILE = 'df_httpclient5-5.0-alpha2-SNAPSHOT.xml'

f = open('feature_list.csv', 'w')
csvWriter = csv.writer(f, lineterminator='\n')
tree = ElementTree.parse(XMLFILE)
root = tree.getroot()
print root.tag
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
            tmp = e_feature.find('name').text
            print e_package_name + ',' + e_class_name + ',' + tmp
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
            info = [e_package_name, e_class_name, e_feature_name]
            csvWriter.writerow(info)
f.close()
