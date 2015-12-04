# -*- coding: utf-8 -*-
"""
this script does all the processing by calling analysis()
I do
    tree_cpy = tree
    while tree == tree_cpy:
        tree = page_getter(driver, XPath, file_name)
everytime that I try to move to other page.
I do this because selenium webdriver doesn't work well sometimes.
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from lxml import html
import sys
import time
import csv
import subprocess

def project_sorter(driver, tree):
    pjt_table = tree.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/table/tbody/tr')
    next_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/table/thead/tr/th[6]/a")
    next_button.click()
    return

def pjt_name_getter(tree):
    pjt_name = tree.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]/a/text()')
    return pjt_name[0]

def initial_setup1():
    driver = webdriver.Firefox()
    driver.implicitly_wait(60)
    driver.get("http://localhost:9000")
    return driver

def initial_setup2(driver):
    html_source = driver.page_source
    f = open("dashboard.html", "w")
    f.write(html_source.encode("utf-8"))
    f.close()
    html_string = open("dashboard.html").read()
    tree = html.fromstring(html_string)
    return tree

def page_getter(driver, xpath, file_name):
    next_button = driver.find_element_by_xpath(xpath)
    next_button.click()
    html_source = driver.page_source
    f = open(file_name, "w")
    f.write(html_source.encode("utf-8"))
    f.close()
    html_string = open(file_name).read()
    tree = html.fromstring(html_string)
    return tree

def error_failure_checker(tree):
    error = tree.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div[2]/div/div[3]/span[2]/a/span/text()')
    failure = tree.xpath('/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div[2]/div/div[2]/span[2]/a/span/text()')
    return int(error[0]), int(failure[0])

def operation_checker(driver, src, dst):
    try:
        result = subprocess.check_output('diff ' + src + ' ' + dst, shell=True)
        return driver, "succcess"
    except subprocess.CalledProcessError:
        driver.back()
        return driver, "failure"

def analysis():
    driver = initial_setup1()
    tree = initial_setup2(driver)
    project_sorter(driver, tree)
    pjt_name = pjt_name_getter(tree)
    print pjt_name
    tree_cpy = tree
    while tree == tree_cpy:
        tree = page_getter(driver, "/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[2]/a", "comprehensive_analysis_result.html")
        print "hoge"
        #driver, flag = operation_checker(driver, "dashboard.html", "comprehensive_analysis_result.html")
    error, failure = error_failure_checker(tree)
    if error >= 0:
        tree_cpy = tree
        while tree == tree_cpy:
            tree = page_getter(driver, "/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div[2]/div/div[3]/span[2]/a/span", "error.html")
        driver.back()
    if failure >= 0:
        tree_cpy = tree
        while tree == tree_cpy:
            tree = page_getter(driver, "/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div[2]/div/div[2]/span[2]/a/span", "failure.html")
        driver.back()
