#!/bin/bash

set -e

SOURCE_FILE=$1
TARGET_DIR=$2

SOURCE_DIR=`dirname $SOURCE_FILE`
#echo SOURCE_DIR=$SOURCE_DIR

IFS='/' CGLIST=($1)
IFS=' '
CGLIST_COUNT=${#CGLIST[*]}
DIR_LAYER=`expr $CGLIST_COUNT - 2`
#echo DIR_LAYER=$DIR_LAYER

FILENAME=${CGLIST[$CGLIST_COUNT-1]}
FILENAME=${FILENAME%.*}
#echo FILENAME=$FILENAME

# 生成多层级的分类列表和文件名的前缀
STR_CGLIST=''
STR_FILEPREFIX=''
for ((i=1;i<=$DIR_LAYER;i++));do
	CGNAME=${CGLIST[$i]}
	STR_FILEPREFIX=${STR_FILEPREFIX}${CGNAME}'-'
	STR_CGLIST=$STR_CGLIST'- '$CGNAME'
'
done
#echo $STR_CGLIST

TARGET_FILE=$TARGET_DIR/${STR_FILEPREFIX}${CGLIST[`expr $CGLIST_COUNT - 1`]}
#echo TARGET_FILE=$TARGET_FILE

# write file
echo "generating... ${FILENAME}"
echo "title: $FILENAME
categories:
$STR_CGLIST
" > "$TARGET_FILE"
cat "$SOURCE_FILE">>"$TARGET_FILE"

# copy images dir
IMG_DIR_SOURCE="${SOURCE_DIR}/_assets/${FILENAME}"
#echo "IMG_DIR_SOURCE=${IMG_DIR_SOURCE}"
IMG_DIR_TARGET=${TARGET_DIR}/${STR_FILEPREFIX}${FILENAME}
#echo IMG_DIR_TARGET=$IMG_DIR_TARGET
if [[ -d "${IMG_DIR_SOURCE}" ]]; then
	#echo "img dir exsit, do copy"
	cp -r $IMG_DIR_SOURCE $IMG_DIR_TARGET
	
	# \!\[(\S*)\]\(test\/(\S*)\)
	# {% asset_img $2 $1 %}\n
	sed -i "s?\\!\\[\(\\S*\)\\](_assets/${FILENAME}/\(\S*\))?{% asset_img \2 \1 %}?g" $TARGET_FILE
	
#else
	#echo "img dir no exsit"
fi

