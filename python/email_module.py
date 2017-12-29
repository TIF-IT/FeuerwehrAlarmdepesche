#!/usr/bin/python
# -*- coding: utf-8 -*-

from registry import ModuleRegistry, Api
import imaplib
import socket
try:
  from HTMLParser import HTMLParser
except ModuleNotFoundError as e:
  from html.parser import HTMLParser
from email.parser import FeedParser
import alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time
import sys


availableAlarmdepescheDefault = { 'Einsatzstichwort':'Einsatzstichwort'
                           , 'AlarmiertesEinsatzmittel':'Einsatzmittel'
                           , 'Sachverhalt':'Sachverhalt'
                           , 'Sondersignal':'Sondersignal'
                           , 'Patientenname':'Patientenname'
                           , 'Einsatzbeginn':'Einsatzbeginn'
                           , 'Einsatznummer':'Einsatznummer'
                           , 'Name':'Name'
                           , 'Zusatz':'Zusatz'
#                           , '':''
                           }
# Einsatzziel
availableAlarmdepescheOperationTarget = { 'Objekt':'Objekt:'
                                        , 'Objekttyp':'Objekttyp'
                                        , 'StrasseHausnummer':'Strasse'
                                        , 'Segment':'Segment'
                                        , 'PLZOrt':'PLZ'
                                        , 'Region':'Region'
                                        , 'Info':'Info'
                                        }
#  Transportziel
availableAlarmdepescheTransportTarget = { 'Transportziel':'Transportziel'
                                        , 'Objekt':'Objekt:'
                                        , 'Objekttyp':'Objekttyp'
                                        , 'StrasseHausnummer':'Strasse'
                                        , 'PLZOrt':'PLZ'
                                        }


@ModuleRegistry.register
class EmailModule(Api):
    """
    Email module
    """

    def getDummyMailBody ():
      file = open("vorlagen/Steinbachhallenberg.html", "r")
      return (999, file.read() )


    def getLastMail ():
      #ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
      #ctx = ssl.SSLContext(PROTOCOL_SSLv3)
      #passwd = getpass.getpass()
      mail =  imaplib.IMAP4_SSL(config.imap['host'], config.imap['port'])
      mail.login(config.imap['user'], config.imap['passwd'])
      mail.select(config.imap['mailBox'], 1)

      result, data = mail.search(None, "ALL")

      ids = data[0] # data is a list.
      id_list = ids.split() # ids is a space separated string
      if len(id_list) == 0:
        return (0, "")

      latest_email_id = id_list[-1] # get the latest

      result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID

      rawMailBody = data[0][1].decode("utf-8")
      f = FeedParser()
      f.feed(rawMailBody)
      rootMessage = f.close()

      mailBody=rootMessage.get_payload(1).get_payload(decode=True)

      mail.close()
      mail.logout()
      del mail

      return (latest_email_id, mailBody.decode("utf-8"))


    def interpretHTMLAlarmdepesche(htmlAlarmdepesche):
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

      return foundAlarmdepesche


if __name__ == '__main__':
    from core import Core
    c = Core()
    obj = c.get_instance(EmailModule)
    assert obj
    lastMailID, mailBody = EmailModule.getDummyMailBody()
    dicAlarmdepesche = EmailModule.interpretHTMLAlarmdepesche(mailBody)
    obj.new_alarm(lastMailID, dicAlarmdepesche)

