#!/bin/sh
# start.sh
# Navigate to script directory, execute python script.
# Makes cronjob a little easier, but not entirely nessicary.

cd /home/pi/psubutton
python3 psubutton.py
