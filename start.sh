#!/bin/bash
#
WORK_DIR_PYTHON=/usr/FeuerwehrAlarmdepesche/app/
#
/usr/bin/mysqld_safe &
sleep 5
python ${WORK_DIR_PYTHON}/parseAlarmMail.py & 
python ${WORK_DIR_PYTHON}/restFullService.py &
#

#
#
