#!/bin/bash

dir="/usr/src/redis-4.0.6"

case $1 in 
start)
	${dir}/src/redis-server ${dir}/redis.conf;;
stop)kill -9 `pgrep redis-server`;;
client) ${dir}/src/redis-cli ${dir}/redis.conf ;;
*) echo "start|stop|restart|client"
esac

pgrep redis-server
