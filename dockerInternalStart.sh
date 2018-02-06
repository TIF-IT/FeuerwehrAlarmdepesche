#!/bin/bash
#
WORK_DIR_PYTHON=/usr/FeuerwehrAlarmdepesche/
#
service mysql start
mysql -u root < ${WORK_DIR_PYTHON}/dbinit.sql
service apache2 start
#python3 -m Alarmdepesche
python3 -m Alarmdepesche Alarmdepesche/__main__.py
