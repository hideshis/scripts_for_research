# -*- coding: utf-8 -*-
import subprocess
import sys
import os
from lxml import etree as ET

def new_tag_insert(parent, order, tag_name, text, attrib_dict):
    new_tag = ET.Element(tag_name)
    if text == '':
        if len(attrib_dict) >= 1:
            for key, value in attrib_dict.items():
                new_tag.attrib[key] = value
            return new_tag
    else:
        new_tag.text = text
        if len(attrib_dict) >= 1:
            for key, value in attrib_dict.items():
                new_tag.attrib[key] = value
    parent.insert(order, new_tag)
    return

def new_tag_append(parent, tag_name, text, attrib_dict):
    new_tag = ET.Element(tag_name)
    if text == '':
        if len(attrib_dict) >= 1:
            for key, value in attrib_dict.items():
                new_tag.attrib[key] = value
            return new_tag
    else:
        new_tag.text = text
        if len(attrib_dict) >= 1:
            for key, value in attrib_dict.items():
                new_tag.attrib[key] = value
    parent.append(new_tag)
    return

def edit_build(build):
    build_children_list = [build_child.tag.split('}')[-1] for build_child in list(build) if True]
    if 'plugins' not in build_children_list:
        plugins_tag = 'plugins'
        new_tag_insert(build, len(list(build)), plugins_tag, '', {})
    else:
        for build_child in list(build):
            if build_child.tag.endswith('plugins'):
                plugins_tag = build_child.tag
                break
    plugins = build.find(plugins_tag)
    new_tag_insert(plugins, 0, 'plugin', '', {})
    plugin = plugins.findall('plugin')[0]
    new_tag_append(plugin, 'groupId', 'org.jacoco', {})
    new_tag_append(plugin, 'artifactId', 'jacoco-maven-plugin', {})
    new_tag_append(plugin, 'version', '0.7.7.201606060606', {})
    new_tag_append(plugin, 'executions', '', {})
    executions = plugin.find('executions')
    new_tag_append(executions, 'execution', '', {})
    execution = executions.find('execution')
    new_tag_append(execution, 'id', 'prepare-agent', {})
    new_tag_append(execution, 'goals', '', {})
    goals = execution.find('goals')
    new_tag_append(goals, 'goal', 'prepare-agent', {})
    return

argvs = sys.argv
pom_file_path = argvs[1]
parser = ET.XMLParser(remove_blank_text=True)
pom = ET.parse(pom_file_path, parser)
root = pom.getroot()
root_children_list = list(root)
insert_location = len(root_children_list)
build_tag = 'build'
for i in range(len(root_children_list)):
    if ET.tostring(root_children_list[i]).startswith('<build'):
        build_tag = root_children_list[i].tag

if root.find(build_tag) == None:
    #build_tag = 'build'
    new_tag_append(root, build_tag, '', {})
    insert_location += 1
edit_build(root.find(build_tag))
pom.write(pom_file_path, pretty_print=True)
