# -*- coding: utf-8 -*-

import MySQLdb
import sys
import csv

if __name__ == "__main__":
    f = open('build_status.csv', 'w')
    csvWriter = csv.writer(f, lineterminator='\n')
    header = ['pjt_name', 'errored', 'passed', 'failed', 'cancelled']
    csvWriter.writerow(header)

    connector = MySQLdb.connect(host="localhost", db="tt_7_9_2016", user="root", passwd="")#, charset="utf8")
    cursor = connector.cursor()

    #sql = "select * from テーブル名"
    #sql = "desc travistorrent_7_9_2016"
    sql = "select distinct gh_project_name from travistorrent_7_9_2016 where tr_analyzer = 'java-maven'"
    cursor.execute(sql)
    records = cursor.fetchall()
    for record in records:
        pjt_name = record[0]
        build_status_count = {'errored':0, 'passed':0, 'failed':0, 'cancelled':0}
        #sql = "select gh_project_name, git_commit, tr_build_id, tr_job_id, tr_status, tr_tests_run, tr_tests_skipped, tr_tests_ok, tr_tests_fail from travistorrent_7_9_2016 where gh_project_name = '" + pjt_name + "'"
        sql = "select tr_tests_ran, tr_tests_failed, count(*) from travistorrent_7_9_2016 where gh_project_name = '" + pjt_name + "'"
        cursor.execute(sql)
        records2 = cursor.fetchall()
        for record2 in records2:
            print pjt_name, record2
        break
    cursor.close()
    connector.close()
    f.close()
