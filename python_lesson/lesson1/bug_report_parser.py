#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script identifies following info.:
1. bug ID

input: Bug report. It is obtained by using Masaki's script.
output: Info. cited above.
"""
# 各ライブラリのインポート
import os
import sys
import commands
import subprocess
import re
from lxml import html

def extraction(file_name):
    # htmlファイルをオープンし，tree 変数にhtmlコードを格納する
    html_string = open(file_name).read()
    tree = html.fromstring(html_string)

    """
    extracting bug ID
    """
    # xpath を指定してテキストをリストオブジェクトとして取得し，bug_id_html 変数に格納する
    bug_id_html = tree.xpath('//*[@id="changeform"]/div[1]/a/b/text()')
    # re ライブラリの findall 関数を使って，上で指定した正規表現に一致する文字列を抽出する
    # 正規表現に一致する文字列は，リストオブジェクトとして match 変数に格納される
    match = re.findall(r'[0-9]+', bug_id_html[0])
    bug_id = match[0]
    print "Bug ID: " + bug_id
    return

if __name__ == "__main__":
    extraction("issue_report_sample.html")
