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

def edit_properties(properties):
    new_tag_append(properties, 'jmockit.version', '1.23', {})
    return

def edit_dependencyManagemt(dependencyManagement):
    new_tag_append(dependencyManagement, 'dependencies', '', {})
    dependencies = dependencyManagement.find('dependencies')
    new_tag_append(dependencies, 'dependency', '', {})
    new_tag_append(dependencies, 'dependency', '', {})
    dependency1 = dependencies.findall('dependency')[-2]
    dependency2 = dependencies.findall('dependency')[-1]
    new_tag_append(dependency1, 'groupId', 'org.jmockit', {})
    new_tag_append(dependency1, 'artifactId', 'jmockit', {})
    new_tag_append(dependency1, 'version', '${jmockit.version}', {})
    new_tag_append(dependency1, 'scope', 'test', {})
    new_tag_append(dependency2, 'groupId', 'org.jmockit', {})
    new_tag_append(dependency2, 'artifactId', 'jmockit-coverage', {})
    new_tag_append(dependency2, 'version', '${jmockit.version}', {})
    new_tag_append(dependency2, 'scope', 'runtime', {})
    new_tag_append(dependency2, 'optional', 'true', {})
    return

def edit_dependencies(dependencies):
    new_tag_insert(dependencies, 0, 'dependency', '', {})
    new_tag_insert(dependencies, len(list(dependencies)), 'dependency', '', {})
    dependency = dependencies.findall('dependency')[0]
    new_tag_append(dependency, 'groupId', 'org.jmockit', {})
    new_tag_append(dependency, 'artifactId', 'jmockit', {})
    dependency = dependencies.findall('dependency')[-1]
    new_tag_append(dependency, 'groupId', 'org.jmockit', {})
    new_tag_append(dependency, 'artifactId', 'jmockit-coverage', {})
    return

def edit_build(build):
    print len(list(build))
    build_children_list = [build_child.tag.split('}')[-1] for build_child in list(build) if True]
    if 'resources' not in build_children_list:
        new_tag_insert(build, 0, 'resources', '', {})
        resources = build.find('resources')
        new_tag_append(resources, 'resource', '', {})
        resource = resources.find('resource')
        new_tag_append(resource, 'directory', 'src/main/resources', {})
        new_tag_append(resource, 'filtering', 'true', {})
        new_tag_append(resource, 'includes', '', {})
        includes = resource.find('includes')
        new_tag_append(includes, 'include', '**/*.properties', {})
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
    new_tag_append(plugin, 'artifactId', 'maven-surefire-plugin', {})
    new_tag_append(plugin, 'version', '2.18.1', {})
    new_tag_append(plugin, 'configuration', '', {})
    configuration = plugin.find('configuration')
    new_tag_append(configuration, 'disableXmlReport', 'true', {})
    new_tag_append(configuration, 'systemPropertyVariables', '', {})
    systemPropertyVariables = configuration.find('systemPropertyVariables')
    new_tag_append(systemPropertyVariables, 'coverage-output', 'html', {})
    new_tag_append(systemPropertyVariables, 'coverage-outputDir', '${project.build.directory}/coverage-report', {})
    new_tag_append(systemPropertyVariables, 'coverage-maxCallPoints', '10000', {})
    return

parser = ET.XMLParser(remove_blank_text=True)
pom = ET.parse("./pom.xml", parser)
root = pom.getroot()
root_children_list = list(root)
insert_location = len(root_children_list)
properties_tag = 'properties'
dependencyManagement_tag = 'dependencyManagement'
dependencies_tag = 'dependencies'
build_tag = 'build'
for i in range(len(root_children_list)):
    #if ET.tostring(root_children_list[i]).startswith('<packaging'):
    #    insert_location = i+1
    #elif ET.tostring(root_children_list[i]).startswith('<properties'):
    if ET.tostring(root_children_list[i]).startswith('<properties'):
        properties_tag = root_children_list[i].tag
    elif ET.tostring(root_children_list[i]).startswith('<dependencyManagement'):
        dependencyManagement_tag = root_children_list[i].tag
    elif ET.tostring(root_children_list[i]).startswith('<dependencies'):
        dependencies_tag = root_children_list[i].tag
    elif ET.tostring(root_children_list[i]).startswith('<build'):
        build_tag = root_children_list[i].tag

if root.find(properties_tag) == None:
    new_tag_insert(root, insert_location, 'properties', '', {})
    insert_location += 1
edit_properties(root.find('properties'))
if root.find(dependencyManagement_tag) == None:
    #dependencyManagement_tag = 'dependencyManagement'
    new_tag_insert(root, insert_location, dependencyManagement_tag, '', {})
    insert_location += 1
edit_dependencyManagemt(root.find(dependencyManagement_tag))
if root.find(dependencies_tag) == None:
    #dependencies_tag = 'dependencies'
    new_tag_append(root, dependencies_tag, '', {})
    insert_location += 1
edit_dependencies(root.find(dependencies_tag))
if root.find(build_tag) == None:
    #build_tag = 'build'
    new_tag_append(root, build_tag, '', {})
    insert_location += 1
edit_build(root.find(build_tag))
pom.write("./pom_modified.xml", pretty_print=True)
