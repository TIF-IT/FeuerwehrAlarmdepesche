#!/bin/bash
#
WORK_DIR_PYTHON=/usr/FeuerwehrAlarmdepesche/Alarmdepesche/
#
/usr/bin/mysqld_safe &
sleep 5
mysql -u root < dbinit.sql
#python3 -m Alarmdepesche
python3 -m Alarmdepesche Alarmdepesche/__main__.py
