#!/bin/bash
workers=10
# This creates the manager machines
echo "======> Creating $workers worker machines ...";
for node in $(seq 1 $workers);
do
	echo "======> Creating worker$node machine ...";
	docker-machine create --driver virtualbox default$node;
done
