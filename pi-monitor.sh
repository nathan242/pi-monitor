#!/bin/bash

RELOAD_DELAY=10
RUN_USER=nathan

function do_exit() {
	echo "Stopping on signal"
	# Kill all children
	for pid in `jobs -p`
	do
		kill $pid
	done

	sleep 2

	exit 0
}

trap do_exit SIGINT SIGTERM

# Start pi-monitor
while true
do
	sudo -u $RUN_USER /opt/pi-monitor/pi-monitor.py
	sleep $RELOAD_DELAY
done

