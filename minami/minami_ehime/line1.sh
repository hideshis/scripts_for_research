#!/bin/sh
# 変数の宣言：(変数名)=(変数の値)　※余計な空白文字は挿入しないこと!!
dir_name=$1
commit_hash=$2
file1=$3
destination=$4
# git コマンドを使って，file1 を昔のバージョンに戻す
# cp コマンドを使って，file1 をdestinationにコピーする
