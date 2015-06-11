#!/bin/sh
# description:  テストコードとプロダクトコードのファイル名リストを作成し，各プロダクトコードに対するテストコードが存在するかを調べる．
# caller:       checkouter.py
# callee:       file_finder.py
#               files_integrator.py
all_code_path="C:/Users/hideshi-s/test_research/eclipse.jdt.core" # ソースコードが格納されているディレクトリへの絶対パス(エスケープを避けるため，パスの区切りはヌル文字ではなくスラッシュにすること．)
project_dir_name="eclipse_jdt_data" # 生成されたファイルを格納するためのディレクトリ
product_code_files=$1
test_code_files=$2
link_file=$3
dir_name=$4
# テストコードとプロダクトコードのファイル名リストを作成する．
echo "hogehoge"
python file_finder.py ${all_code_path} ${product_code_files} ${test_code_files}
# プロダクトコードに対するテストコードが存在するかを調べ，リンク情報を作成する．
python files_integrator.py ${product_code_files} ${test_code_files} ${link_file}
# データ保管用のディレクトリを作成し，生成されたファイル群をコピーまたは移動する．
mkdir ${dir_name}
mv ${product_code_files} ${dir_name}
mv ${test_code_files} ${dir_name}
cp ${link_file} ${project_dir_name}
mv ${link_file} ${dir_name}
mv ${dir_name} ${project_dir_name}
