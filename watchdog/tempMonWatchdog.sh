#!/bin/bash

# 2018/10 BuRnCycL
# Watchdog script for Temperature Monitor. Works in conjunction with a crontab to insure Temperature Monitor stays
# running on screen background. Use screen -r to reattach. CTRL+A+D to detach.

NAME="temperaturemon"
PROCESS_ID=`ps -ef|egrep SCREEN|egrep ${NAME}|awk '{print $2}'`
SCREEN="/usr/bin/screen"
SCRIPT_DIR="/usr/local/sbin"
SCRIPT="temperatureMon.py"

if [ -z "$PROCESS_ID" ];then
       echo "Temperature Monitor not running. Starting..."
       $SCREEN -dmS temperaturemon python3 ${SCRIPT_DIR}/${SCRIPT}
else
        echo "Temperature Monitor is running."
fi

