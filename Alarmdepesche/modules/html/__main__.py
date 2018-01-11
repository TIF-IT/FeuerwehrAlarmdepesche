#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.core import Core
from Alarmdepesche.modules.html import html_module

c = Core()
obj = c.get_instance(html_module.HtmlModule)
assert obj
while True:
    pass
