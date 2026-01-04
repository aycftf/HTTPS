#!/usr/bin/env bash

read -p "Enter dest. address for local https server to pull file from: " ip
read -p "Enter port: " port

curFile=$(curl -q -k https://"$ip":"$port" -i |grep "Content-Disposition"| cut -d ' ' -f3)
echo -e "\n Current File being hosted: $curFile \n"
read -p "Enter File Name and File Trailer here (Ex: linux.zip): " fileName
read -p "Enter New File Name and Trailer here (Ex: newlinux.zip):  " newFile
if curl https://"$ip":"$port"/"$fileName" -k -v -o "$newFile"; then
	echo -e "File download sucess! "
	ls -lah | grep "newFile.zip"  && exit 0



else
	echo -e "File did NOT extract / curl properly... try again.. " && exit 1


fi
