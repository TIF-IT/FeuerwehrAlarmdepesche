#!/usr/bin/python

import imaplib
import socket
import ssl
from HTMLParser import HTMLParser
from email.parser import FeedParser
import alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time

import sys

reload(sys)
sys.getdefaultencoding()

availableAlarmdepescheDefault = { 'Einsatzstichwort':'Einsatzstichwort'
                           , 'AlarmiertesEinsatzmittel':'Einsatzmittel'
                           , 'Sondersignal':'Sondersignal'
                           , 'Einsatzbeginn':'Einsatzbeginn'
                           , 'Einsatznummer':'Einsatznummer'
                           , 'Objekt':'Objekt:'
                           , 'Objekttyp':'Objekttyp'
                           , 'StrasseHausnummer':'Strasse'
                           , 'Segment':'Segment'
                           , 'PLZOrt':'PLZ'
                           , 'Region':'Region'
                           , 'Info':'Info'
                           , 'Name':'Name'
                           , 'Zusatz':'Zusatz'
#                           , '':''
                           }

availableAlarmdepescheOperationTarget = {  }

availableAlarmdepescheTransportTarget = {  }


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
  print (mailBody)

  mail.close()
  mail.logout()
  del mail

  return (latest_email_id, mailBody)

# =====================================================

def interpretHTMLAlarmdepesche ( htmlAlarmdepesche ):
  soup = BeautifulSoup(htmlAlarmdepesche, "lxml")
  table = soup.find("table", attrs={})

#  datasets = []
#  for row in table.find_all("tr")[1:]:
#    dataset = [td.get_text() for td in row.find_all("td")]
#    datasets.append(dataset)

  datasets = []
  for row in soup.find_all("tr")[1:]:
    dataset = [td.get_text() for td in row.find_all("td")]
    datasets.append(dataset)

  print datasets


  foundAlarmdepesche = {}
  operationTarget = {}
  transportDestination = {}

  isDefault = True
  isOperationTarget = False
  isTransportTarget = False

  for dataset in datasets:
    for alarmdepItem in availableAlarmdepesche:
      item = dataset[1].encode('utf-8').rstrip()#dataset[1].decode("utf-8", 'ignore').rstrip()
#      if dataset[0] == availableAlarmdepesche[alarmdepItem]:
      if dataset[0].find(availableAlarmdepesche[alarmdepItem]) != -1:
        foundAlarmdepesche[alarmdepItem] = item 

  print foundAlarmdepesche

  return foundAlarmdepesche

# TODO: 
def createSQLFromDict ( lastMailID, dicAlarmdepesche ):
  sqlQuery = "insert into Alarmdepesche (messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Objekt, Objekttyp, StrasseHausnummer, Segment, PLZOrt, Region, Info, Name, Zusatz) VALUES ("

  sqlQuery += str(lastMailID)+","

#  for depesche in availableAlarmdepesche:
#    if depesche in dicAlarmdepesche.keys():
#      sqlQuery += "\""+dicAlarmdepesche[depesche]+"\","
#    else:
#      sqlQuery += "\"\","


  if 'Einsatzstichwort' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Einsatzstichwort"]+"\","
  else:
    sqlQuery += "\"\","
  if 'AlarmiertesEinsatzmittel' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["AlarmiertesEinsatzmittel"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Sondersignal' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Sondersignal"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Einsatzbeginn' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Einsatzbeginn"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Einsatznummer' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Einsatznummer"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Objekt' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Objekt"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Objekttyp' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Objekttyp"]+"\","
  else:
    sqlQuery += "\"\","
  if 'StrasseHausnummer' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["StrasseHausnummer"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Segment' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Segment"]+"\","
  else:
    sqlQuery += "\"\","
  if 'PLZOrt' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["PLZOrt"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Region' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Region"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Info' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Info"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Name' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Name"]+"\","
  else:
    sqlQuery += "\"\","
  if 'Zusatz' in dicAlarmdepesche:
    sqlQuery += "\""+dicAlarmdepesche["Zusatz"]+"\""
  else:
    sqlQuery += "\"\""

  #sqlQuery += "\""+dicAlarmdepesche[""]+"\","


  sqlQuery += ");"

  #print (sqlQuery)

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

while True:
  runCheckup ()
  time.sleep(int(config.imap['checkIntervall']))

