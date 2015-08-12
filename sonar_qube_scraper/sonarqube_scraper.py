# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from lxml import html
import sys
import time
import csv

def file_output(pc_list):
    writer = csv.writer(file("pc_name_coverage_list.csv", 'a'), lineterminator="\n")
    for pc_info in pc_list:
        writer.writerow(pc_info)
    return

def pc_name_coverage_getter(driver, sub_system_name, module_name):
    coverage_table = []
    while len(coverage_table) == 0:
        f = open("target.html", "w")
        html_source = driver.page_source
        f.write(html_source.encode("utf-8"))
        f.close()
        html_string = open("target.html").read()
        tree = html.fromstring(html_string)
        coverage_table = tree.xpath('//*[@id="col_2"]/table/tbody/tr')
        print len(coverage_table)
        return_list = []
        for x in range(len(coverage_table)):
            pc_name = tree.xpath('//*[@id="col_2"]/table/tbody/tr[' + str(x+1) + ']/td[1]/a[2]/text()')[0]
            pc_name = module_name + "/" + pc_name
            pc_coverage= tree.xpath('//*[@id="col_2"]/table/tbody/tr[' + str(x+1) + ']/td[2]/span/text()')[0]
            print "        " + pc_name + " " + pc_coverage
            pc_info = []
            pc_info.append(pc_name)
            pc_info.append(pc_coverage)
            return_list.append(pc_info)
        if len(coverage_table) == 0:
            print "retry @ pc_name_coverage_getter"
    file_output(return_list)
    return return_list

def module_crawler(driver, sub_system_name):
    html_string = open("hogehoge2.html").read()
    tree = html.fromstring(html_string)
    module_table = tree.xpath('//*[@id="col_1"]/table/tbody/tr')
    finish_counter = 0
    for x in range(len(module_table)):
        pc_list = []
        while len(pc_list) == 0:
            module_name = tree.xpath('//*[@id="col_1"]/table/tbody/tr[' + str(x+1) + ']/td[1]/a[2]/text()')[0]
            print "    " + module_name
            next_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div[2]/table/tbody/tr/td[2]/div/table/tbody/tr[' + str(x+1) + ']/td[1]/a[2]')
            next_button.click()
            pc_list = pc_name_coverage_getter(driver, sub_system_name, module_name)
            if len(pc_list) == 0:
                print "retry @ module_crawler"
                driver.back()
            else:
                finish_counter += 1
    return driver, finish_counter

def html_parser(driver):
    html_string = open("hogehoge.html").read()
    tree = html.fromstring(html_string)
    sub_system_table = tree.xpath('/html/body/div[1]/div/div/div[4]/div[2]/table/tbody/tr/td[1]/div/table/tbody/tr')
    print sub_system_table
    finish_counter = 0
    for x in range(len(sub_system_table)):
        num = 0
        while num == 0:
            sub_system_name = tree.xpath('/html/body/div[1]/div/div/div[4]/div[2]/table/tbody/tr/td[1]/div/table/tbody/tr[' + str(x+1) + ']/td[1]/a[2]/text()')
            print sub_system_name
            next_button = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div[2]/table/tbody/tr/td[1]/div/table/tbody/tr[' + str(x+1) + ']/td[1]/a[2]')
            next_button.click()
            f = open("hogehoge2.html", "w")
            html_source = driver.page_source
            f.write(html_source.encode("utf-8"))
            f.close()
            driver, num = module_crawler(driver, sub_system_name)
            if num == 0:
                print "retry @ html_parser"
                driver.back()
            else:
                finish_counter += 1
    return driver, finish_counter

driver = webdriver.Firefox()
driver.implicitly_wait(60)
driver.get("http://localhost:9000")
next_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[8]/td[2]/a")
next_button.click()
next_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div[1]/div[2]/div/div[4]/div/div[1]/div[1]/div[1]/div/div[1]/span[2]/a")
next_button.click()
html_source = driver.page_source
f = open("hogehoge.html", "w")
f.write(html_source.encode("utf-8"))
f.close()
num = 0
while num == 0:
    driver, num = html_parser(driver)
    if num == 0:
        print "retry @ main function."
