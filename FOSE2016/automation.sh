#!/bin/bash
git_repo_url="/Users/hideshi-s/Desktop/exp/result/15/0626seminar2/httpclient/original.git"
git_dir_name="./original.git"
buggy_commit_list=(`cat ./bug_location/buggy_commit_list.csv`)
for buggy_commit in ${buggy_commit_list[@]};
do
  cp -a $git_repo_url ./
  cd $git_dir_name
  git checkout $buggy_commit
  exit 0
  cd ..
  rm -rf $git_dir_name
done;
