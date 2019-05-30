#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from Alarmdepesche.registry import ModuleRegistry, Api
import imaplib
import socket
#try:
#  from HTMLParser import HTMLParser
#except ModuleNotFoundError as e:
from html.parser import HTMLParser
from email.parser import FeedParser
import Alarmdepesche.alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time
import re


availableAlarmdepescheDefault = { 'Einsatzstichwort':'Einsatzstichwort'
                           , 'AlarmiertesEinsatzmittel':'Einsatzmittel'
                           , 'Sachverhalt':'Sachverhalt'
                           , 'Sondersignal':'Sondersignal'
                           , 'Patientenname':'Patientenname'
                           , 'Einsatzbeginn':'Einsatzbeginn'
                           , 'Einsatznummer':'Einsatznummer'
                           , 'Auftragsnummer':'Auftragsnummer'
                           , 'Name':'Name'
                           , 'Zusatz':'Zusatz'
                           }
# Einsatzziel
availableAlarmdepescheOperationTarget = { 'Objekt':'Objekt:'
                                        , 'Objekttyp':'Objekttyp'
                                        , 'StrasseHausnummer':'Strasse'
                                        , 'Segment':'Segment'
                                        , 'PLZOrt':'PLZ'
                                        , 'Region':'Region'
                                        , 'Info':'Info'
                                        #, 'Geopositionen':'Geopositionen'
                                        }
#  Transportziel
availableAlarmdepescheTransportTarget = { 'Transportziel':'Transportziel'
                                        , 'Objekt':'Objekt:'
                                        , 'Objekttyp':'Objekttyp'
                                        , 'StrasseHausnummer':'Strasse'
                                        , 'Segment':'Segment'
                                        , 'PLZOrt':'PLZ'
                                        , 'Region':'Region'
                                        , 'Info':'Info'
                                        #, 'Geopositionen':'Geopositionen'
                                        }


@ModuleRegistry.register
class EmailModule(Api):
    """
    Email module
    """

    def config(self):
        while True:
            self.runCheckup()
            time.sleep(int(config.imap['checkIntervall']))


    def runCheckup(self):
      #print ("Check for mail")
      lastMailID, mailBody = self.getLastMail()

      #print ("MailBody: " + mailBody)
      if lastMailID != 0:
          dicAlarmdepesche = self.interpretHTMLAlarmdepesche(mailBody)
          self.new_alarm(lastMailID, dicAlarmdepesche)

    def getDummyMailBody(self):
      #file = open("vorlagen/Steinbachhallenberg.html", "r", encoding='utf-8')
      #file = open("vorlagen/Leinefelde_Test-Alarm.html", "r", encoding='utf-16')
      file = open("vorlagen/Leinefelde_DemoGen.html", "r", encoding='utf-8')
      return (999, file.read() )


    def getLastMail(self):
      #ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
      #ctx = ssl.SSLContext(PROTOCOL_SSLv3)
      #passwd = getpass.getpass()
      try:
        mail = imaplib.IMAP4_SSL(config.imap['host'], config.imap['port'])
        mail.login(config.imap['user'], config.imap['passwd'])
        mail.select(config.imap['mailBox'], 1)
      except:
        print ("!Error with mail connection")

      try:
        result, data = mail.search(None, "ALL")

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        if len(id_list) == 0:
          return (0, "")

        latest_email_id = id_list[-1] # get the latest

        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

        rawMailBody = data[0][1].decode("utf-8")
        #rawMailBody = data[0][1]
        #print (rawMailBody)
        f = FeedParser()
        f.feed(rawMailBody)
        rootMessage = f.close()

        #print ("rootMessage: "+str(rootMessage.get_payload(0)))

        mailBody=rootMessage.get_payload(1).get_payload(decode=True)

        mail.close()
        mail.logout()
        del mail

        return (latest_email_id, mailBody.decode("utf-8"))
        #return (latest_email_id, mailBody.decode("utf-16"))
      except:
        print ("!Error with mail select")
        return (0, "")


    def interpretHTMLAlarmdepesche(self, htmlAlarmdepesche):
      soup = BeautifulSoup(htmlAlarmdepesche, "lxml")
      table = soup.find("table", attrs={})

      tables = []
      for table in soup.find_all("table"):
        datasets = []
        for row in table.find_all("tr")[1:]:
          dataset = [td.get_text() for td in row.find_all("td")]
          datasets.append(dataset)
        tables.append(datasets)

      foundAlarmdepesche = {'Default':{},'Einsatzziel':{},'Transportziel':{}}

      for datasets in tables:
        for dataset in datasets:
          availableAlarmdepesche = availableAlarmdepescheDefault
          identifier = "Default"
          # Einsatzziel
          if "Einsatzziel" in datasets[0][0]:
            availableAlarmdepesche = availableAlarmdepescheOperationTarget
            identifier = "Einsatzziel"
          # Transportziel
          elif "Transportziel" in datasets[0][0]:
            availableAlarmdepesche = availableAlarmdepescheTransportTarget
            identifier = "Transportziel"

          for alarmdepItem in availableAlarmdepesche:
            if len(dataset) > 1 and availableAlarmdepesche[alarmdepItem] in dataset[0]:
              foundAlarmdepesche[identifier][alarmdepItem] = dataset[1].strip()

      print (foundAlarmdepesche)

      (htmlAlarmdepesche, foundAlarmdepesche) = ModuleRegistry.callExtensionPoints("HTML_INTERPRETED", (htmlAlarmdepesche, foundAlarmdepesche))

      return foundAlarmdepesche


