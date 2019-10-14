#!/bin/sh
url_list=(http://www.bbc.co.uk http://www.cnn.com http://www.msn.com http://google.com http://rit.edu http://192.168.1.11:23000 https://amazon.com https://youtube.com https://yaf.org)
while [ 1 ]; do
	for i in ${url_list[@]}; do
		rm index.html
		sleep $[ ( $RANDOM % 10 )  + 1 ]s	
		wget 192.168.1.11:23000

		echo "pulling ${i}"	
		sleep $[ ( $RANDOM % 10 )  + 1 ]s
		echo "here"
		nslookup $i
	done
done
