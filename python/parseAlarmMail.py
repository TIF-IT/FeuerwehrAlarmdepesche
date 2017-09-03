#!/usr/bin/python3

import imaplib
import socket
import ssl
from HTMLParser import HTMLParser
from email.parser import FeedParser
import alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time

# https://stackoverflow.com/questions/25318012/how-to-connect-with-python-imap4-ssl-and-self-signed-server-ssl-cert

def getLastMail ():
  ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  
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
  ##print (mailBody)

  mail.close()
  mail.logout()
  del mail

  return (latest_email_id, mailBody)

# =====================================================

def interpretHTMLAlarmdepesche ( htmlAlarmdepesche ):
  soup = BeautifulSoup(htmlAlarmdepesche, "lxml")
  table = soup.find("table", attrs={})

  datasets = []
  for row in table.find_all("tr")[1:]:
    dataset = [td.get_text() for td in row.find_all("td")]
    datasets.append(dataset)

  #print datasets

  availableAlarmdepesche = { 'Einsatzstichwort':'Einsatzstichwort:'
                           , 'AlarmiertesEinsatzmittel':'Alarmiertes Einsatzmittel:'
                           , 'Sondersignal':'Sondersignal:'
                           , 'Einsatzbeginn':'Einsatzbeginn(Soll):'
                           , 'Einsatznummer':'Einsatznummer:'
                           , 'Objekt':'Objekt:'
                           , 'Objekttyp':'Objekttyp:'
                           , 'StrasseHausnummer':'Strasse / Hausnummer:'
                           , 'Segment':'Segment:'
                           , 'PLZOrt':'PLZ / Ort:'
                           , 'Region':'Region:'
                           , 'Info':'Info:'
                           , 'Name':'Name:'
                           , 'Zusatz':'Zusatz:'
#                           , '':''
                           }

  foundAlarmdepesche = {}

  for dataset in datasets:
    for alarmdepItem in availableAlarmdepesche:
      if dataset[0] == availableAlarmdepesche[alarmdepItem]:
        foundAlarmdepesche[alarmdepItem] = dataset[1].rstrip()

  #print foundAlarmdepesche

  return foundAlarmdepesche

def createSQLFromDict ( lastMailID, dicAlarmdepesche ):
  sqlQuery = "insert into Alarmdepesche (messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Objekt, Objekttyp, StrasseHausnummer, Segment, PLZOrt, Region, Info, Name, Zusatz) VALUES ("

  sqlQuery += str(lastMailID)+","
  sqlQuery += "\""+dicAlarmdepesche["Einsatzstichwort"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["AlarmiertesEinsatzmittel"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Sondersignal"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Einsatzbeginn"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Einsatznummer"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Objekt"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Objekttyp"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["StrasseHausnummer"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Segment"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["PLZOrt"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Region"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Info"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Name"]+"\","
  sqlQuery += "\""+dicAlarmdepesche["Zusatz"]+"\""

  #sqlQuery += "\""+dicAlarmdepesche[""]+"\","


  sqlQuery += ");"

  return sqlQuery

def insertAlarmdepescheIntoDB ( dicAlarmdepesche, sqlAlarmdepesche ):
  # config.mysql['host'] , user, passwd, dbName
  # https://www.tutorialspoint.com/python/python_database_access.htm
  db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'] )
  cursor = db.cursor()
  try:
    sqlStatement = "select id from Alarmdepesche where Einsatznummer='"+dicAlarmdepesche["Einsatznummer"]+"';"
    #print "Select> "+sqlStatement
    cursor.execute(sqlStatement)
    results = cursor.fetchall()
    #print results
    row_count = cursor.rowcount
    if row_count == 0:
      print ("Found new Alarmdepesche")
      cursor.execute(sqlAlarmdepesche)
      db.commit()
    else: 
      print ("The Alarmdepesche is already existing")
  except:
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

while True:
  runCheckup ()
  time.sleep(int(config.imap['checkIntervall']))

