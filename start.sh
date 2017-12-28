#!/bin/bash
#
WORK_DIR_PYTHON=/usr/FeuerwehrAlarmdepesche/app/
python ${WORK_DIR_PYTHON}/parseAlarmMail.py & 
python ${WORK_DIR_PYTHON}/restFullService.py &
#

#
#
