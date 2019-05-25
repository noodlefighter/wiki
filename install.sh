#!/bin/bash

set -e

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

npm install hexo -g

cd $SHELL_FOLDER/hexo
npm install


