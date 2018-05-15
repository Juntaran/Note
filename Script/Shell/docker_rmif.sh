#!/bin/sh 


docker rmi $1 > $1.txt 2>&1
containerid=`cat $1.txt | awk {'print $NF'}`
docker stop $containerid
docker rm $containerid
docker rmi $1
rm -rf $1.txt
