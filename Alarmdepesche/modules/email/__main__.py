#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.core import Core
from Alarmdepesche.modules.email import email_module

c = Core()
obj = c.get_instance(email_module.EmailModule)
assert obj
lastMailID, mailBody = obj.getDummyMailBody()
dicAlarmdepesche = obj.interpretHTMLAlarmdepesche(mailBody)
obj.new_alarm(lastMailID, dicAlarmdepesche)

