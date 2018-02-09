#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.core import Core
from Alarmdepesche.modules.html import html_module

from waiting import wait

c = Core()
obj = c.get_instance(html_module.HtmlModule)
assert obj
wait(lambda : False)
