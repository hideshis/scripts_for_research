# -*- coding: utf-8 -*-
import os

f = open('minami.csv', 'r')
line = f.readline()
line = line.replace('\r', '')
line = line.replace('\n', '')
while line:
    factor = line.split(',')
    setID = factor[0]
    commit_hash = factor[1]
    file1 = factor[2]
    file2 = factor[3]
    # minami script starts here
    if file2 == "hogehoge":
        os.mkdir(setID)
        # file1 を前のバージョンにもどして, setID ディレクトリにコピーする
        destination =  './' + setID  + '/' + file_name_current.split('.')[0] + '_old.java
        os.system('./line1.sh', setID, commit_hash, file1, destination)
    elif file1 == "hogehoge":
        # 上の処理を参考にして自分で書いてください
    else:
        # 上の処理を参考にして自分で書いてください

    line = f.readline()
    line = line.replace('\r', '')
    line = line.replace('\n', '')

"""
cp コマンドの使い方
cp (file_name) (destination)

アルゴリズムの作成
1..一行目を読み込む
3.IDの番号を取り出す
4.IDの番号を名前としたディレクトリを作成する
5.file1のfoo.javaをcommit hash1に戻す git checkout    hash値
6.cp foo.java ディレクトリへ
7.二行目を読み込む
8.var.javaを前のバージョンに戻す
9.va.javaをディレクトリにコピー
10.３行目を読み込む
11.foo.javaのバージョンを戻してコピーする
12.var.javaのバージョンを戻してコピーする
1回のループ　＝　1つの行に対する処理
"""






    #os.system('command here')
    #result = suprocess.check_output('command here', shell=True)
    # minami script ends here
