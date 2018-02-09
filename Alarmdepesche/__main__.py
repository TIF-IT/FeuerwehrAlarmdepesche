#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.core import Core
from Alarmdepesche.modules.email import email_module
from Alarmdepesche.modules.html import html_module
from Alarmdepesche.modules.database import database_module

from waiting import wait


if __name__ == '__main__':
    c = Core()
    wait(lambda : False)
