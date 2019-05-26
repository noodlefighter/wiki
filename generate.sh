#!/bin/bash

#
# 文件名和目录名不允许带空格! 不想处理这种特殊情况了, 垃圾shell脚本
#

set -e

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
SOURCE_FOLDER=$SHELL_FOLDER/source
BUILD_FOLDER=$SHELL_FOLDER/build
TARGET_FOLDER=$SHELL_FOLDER/hexo/source/_posts

rm -rf $BUILD_FOLDER
mkdir -p $BUILD_FOLDER

echo "=============================="
echo " generate file"
echo "=============================="
cd $SOURCE_FOLDER
find -name "*.md" -print0|xargs -0 -i $SHELL_FOLDER/scripts/do_copy.sh {} $BUILD_FOLDER

echo "=============================="
echo " copy to _post"
echo "=============================="
mkdir -p $TARGET_FOLDER
rm -vrf $TARGET_FOLDER/*
cp -vr $BUILD_FOLDER/* $TARGET_FOLDER

# call hexo
cd $SHELL_FOLDER/hexo
hexo g
