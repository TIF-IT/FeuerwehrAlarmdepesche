#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
from Alarmdepesche.registry import ModuleRegistry, Api
#import imaplib
#import socket
#try:
#  from HTMLParser import HTMLParser
#except ModuleNotFoundError as e:
#  from html.parser import HTMLParser
#from email.parser import FeedParser
import Alarmdepesche.alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time

@ModuleRegistry.register
class SampleEmailExtensionModule(Api):
    """
    Email extension module
    """

    def config(self):
        ModuleRegistry.registerExtensionPoint("HTML_INTERPRETED", self.interpretHTMLAlarmdepesche)
#        while True:
#            self.runCheckup()
#            time.sleep(int(config.imap['checkIntervall']))

    def interpretHTMLAlarmdepesche(self, extensionObject):
      (htmlAlarmdepesche, foundAlarmdepesche) = extensionObject
      soup = BeautifulSoup(htmlAlarmdepesche, "lxml")
      #table = soup.find("table", attrs={})

      print ("Run extension for email parsing")

      return (htmlAlarmdepesche, foundAlarmdepesche)


