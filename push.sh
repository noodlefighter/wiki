#!/bin/bash


set -e
set -x

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER

git pull --rebase --autostash
git add --all
git commit -am "quick commit"
git push

