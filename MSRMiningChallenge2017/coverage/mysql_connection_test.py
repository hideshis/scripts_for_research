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
    finish_counter = 0
    for record in records:
        pjt_name = record[0]
        build_status_count = {'errored':0, 'passed':0, 'failed':0, 'cancelled':0}
        #sql = "select gh_project_name, git_commit, tr_build_id, tr_job_id, tr_status, tr_tests_run, tr_tests_skipped, tr_tests_ok, tr_tests_fail from travistorrent_7_9_2016 where gh_project_name = '" + pjt_name + "'"
        sql = "select tr_status, count(tr_status) from travistorrent_7_9_2016 where gh_project_name = '" + pjt_name + "' group by tr_status"
        cursor.execute(sql)
        records2 = cursor.fetchall()
        for record2 in records2:
            if record2[0] == 'errored':
                build_status_count['errored'] = record2[1]
            elif record2[0] == 'passed':
                build_status_count['passed'] = record2[1]
            elif record2[0] == 'failed':
                build_status_count['failed'] = record2[1]
            elif record2[0] == 'canceled':
                build_status_count['cancelled'] = record2[1]
            else:
                print 'this build did not error, pass, fail, and cancell!!'
                print record2
                sys.exit()
        build_status_info = []
        build_status_info.append(pjt_name)
        build_status_info.append(build_status_count['errored'])
        build_status_info.append(build_status_count['passed'])
        build_status_info.append(build_status_count['failed'])
        build_status_info.append(build_status_count['cancelled'])
        csvWriter.writerow(build_status_info)
        finish_counter += 1
        print str(finish_counter), pjt_name, build_status_count
        #break
    cursor.close()
    connector.close()
    f.close()
