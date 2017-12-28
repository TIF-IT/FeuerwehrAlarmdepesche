#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import imaplib
import socket
#import ssl
try:
  from HTMLParser import HTMLParser
except ModuleNotFoundError as e:
  from html.parser import HTMLParser
from email.parser import FeedParser
import alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time
import requests
#from OpenSSL import crypto
#from OpenSSL import SSL as ossl

import sys

#reload(sys)
#sys.getdefaultencoding()

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



# https://stackoverflow.com/questions/25318012/how-to-connect-with-python-imap4-ssl-and-self-signed-server-ssl-cert

def getLastMail ():
  //ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
  //ctx = ssl.SSLContext(PROTOCOL_SSLv3)
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

  f = FeedParser()
  f.feed(data[0][1])
  rootMessage = f.close()

  mailBody=rootMessage.get_payload(1).get_payload(decode=True)
#  print (mailBody)

  mail.close()
  mail.logout()
  del mail

  return (latest_email_id, mailBody)

# =====================================================

def interpretHTMLAlarmdepesche ( htmlAlarmdepesche ):
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

def createSQLFromDict ( lastMailID, dicAlarmdepesche ):
  sqlQuery = ""
  names_list = ["Default", "Einsatzziel", "Transportziel"]
  target_pre = "Target_"
  trans_pre  = "TransTarget_"
  default    = ["Einsatzstichwort", "AlarmiertesEinsatzmittel", "Sondersignal", "Einsatzbeginn", "Einsatznummer", "Name", "Zusatz", "Sachverhalt", "Patientenname"]
  target     = ["Objekt", "Objekttyp", "StrasseHausnummer", "Segment", "PLZOrt", "Region", "Info"]
  trans      = ["Transportziel", "Objekt", "Objekttyp", "StrasseHausnummer", "PLZOrt"]
  combined   = { names_list[0] : default,
                 names_list[1] : target,
                 names_list[2] : trans}

  names  = ['messageID']
  names += default
  names += [target_pre + x for x in  target]
  names += [trans_pre + x for x in trans]

  #sqlQuery += ",".join(["\"" + dicAlarmdepesche.get(x, {}).get(entry, "") + "\"" for x in names for entry in combined[x]])
  values = [str(lastMailID)]
  for x in names_list:
    for entry in combined[x]:
        values.append("\"" + dicAlarmdepesche.get(x, {}).get(entry, "") + "\"")

  try:
    sqlQuery = "insert into {} ({}) VALUES ({});".format(
          "Alarmdepesche",
          ", ".join(names),
          ",".join(values))

  except UnicodeEncodeError as e:
    print ("Value ascii error: " + str(e))

  return sqlQuery

def insertAlarmdepescheIntoDB ( dicAlarmdepesche, sqlAlarmdepesche ):
  # config.mysql['host'] , user, passwd, dbName
  # https://www.tutorialspoint.com/python/python_database_access.htm
  db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'] )
  cursor = db.cursor()
  try:
    subDicAlarmdepesch = dicAlarmdepesche['Default'] if 'Default' in dicAlarmdepesche else {"Einsatznummer":0}
    sqlStatement = "select id from Alarmdepesche where Einsatznummer='"+subDicAlarmdepesch["Einsatznummer"]+"';"
    #print "Select> "+sqlStatement
    cursor.execute(sqlStatement)
    results = cursor.fetchall()
  except Exception as e:
    print(e)
    print ("!Error in select sql statement")
  try:
    #print results
    row_count = cursor.rowcount
    if row_count == 0:
      print ("Found new Alarmdepesche")
#      print (sqlAlarmdepesche) #.decode('utf-8', 'ignore'))
      cursor.execute(sqlAlarmdepesche)
      db.commit()
    else:
      print ("The Alarmdepesche is already existing")
  #except:
  except Exception as e:
    print(e)
    print ("!Error in mysql statement")
    db.rollback()

  db.close()

def runCheckup ():
  print ("Check for mail")
  lastMailID, mailBody = getLastMail ()
  if lastMailID != 0:
    dicAlarmdepesche    = interpretHTMLAlarmdepesche ( mailBody )
    sqlAlarmdepesche     = createSQLFromDict ( lastMailID, dicAlarmdepesche )
    insertAlarmdepescheIntoDB ( dicAlarmdepesche, sqlAlarmdepesche )

if __name__ == "__main__":
    while True:
      runCheckup ()
time.sleep(int(config.imap['checkIntervall']))
