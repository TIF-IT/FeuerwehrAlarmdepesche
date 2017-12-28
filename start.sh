#!/bin/bash
#
WORK_DIR_PYTHON=/usr/FeuerwehrAlarmdepesche/app/
#
/usr/bin/mysqld_safe &
sleep 5
mysql -u root < dbinit.sql
python ${WORK_DIR_PYTHON}/parseAlarmMail.py & 
python ${WORK_DIR_PYTHON}/restFullService.py &
#

#
#
