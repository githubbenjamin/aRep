#!/bin/sh

BCH=`ifconfig | grep 10.175 | awk '{print $6}'`
#LH=`ifconfig | grep 10.175 | awk '{print $2}'`
#echo ${BCH}
#echo ${LH}

ping -c 2 ${BCH} > bch.txt

awk '{if($1==64){ip=substr($4,1,length($4)-1);print ip}}' bch.txt > data.txt

while   read   data;   do
#if [ $data != "" ]; then
#    print $data
    echo "$data"
    nc -w 2 -n -z $data 1-1999 >> scannerResult.txt
#fi
done   <   data.txt
