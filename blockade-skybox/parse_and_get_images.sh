#!/bin/sh
PROMPT_FILE=$1
echo $PROMPT_FILE
for LAB_URL in $(grep -i https $PROMPT_FILE|sed 's/[^/]*\(https:\/\/\)/\1/'); do
	echo $LAB_URL;
	IMAGE_FILE="$(echo $LAB_URL|sed 's/.*\///').jpg";
	echo $IMAGE_FILE;
	URL=$(curl $LAB_URL | grep file_url | sed 's/.*file_url\\":\\"//' | sed 's/\\",\\"thumb_url.*//'|sed 's/\?.*//'); 
	wget -nc -O $IMAGE_FILE $URL
done;
