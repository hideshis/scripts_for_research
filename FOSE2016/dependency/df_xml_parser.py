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
            e_feature_name = e_feature.find('name').text
            if e_feature_name == None:
                e_feature_name = 'no_feature_name'
            print e_package_name + ',' + e_class_name + ',' + e_feature_name
            info = [e_package_name, e_class_name, e_feature_name]
            csvWriter.writerow(info)
f.close()
