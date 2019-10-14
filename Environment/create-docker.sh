#!/bin/bash
workers=10
# This creates the manager machines
echo "======> Creating $workers worker machines ...";
for node in $(seq 1 $workers);
do
	echo "======> Creating worker$node machine ...";
	docker create -it --net host --name worker$node alpine /bin/sh;
done

echo "======> Starting $workers worker machines ...";
for node in $(seq 1 $workers);
do
	echo "======> Starting worker$node machine ...";
	docker container start worker$node;
done


#echo "======> Removing $workers worker machines ...";
#for node in $(seq 1 $workers);
#do
#	echo "======> Starting worker$node machine ...";
#	docker container rm worker$node;
#done
