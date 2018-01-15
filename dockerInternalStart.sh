#!/bin/bash
#

/usr/bin/mysqld_safe &
sleep 5
mysql -u root < dbinit.sql
python -m Alarmdepesche
