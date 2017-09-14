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
#  print (mailBody)

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

  tables = []
  count = 0
  for table in soup.find_all("table")[1:]:
    datasets = []
    for row in table.find_all("tr")[1:]:
      dataset = [td.get_text() for td in row.find_all("td")]
      datasets.append(dataset)
    tables.append((count,datasets))
    count = count + 1
#  for row in soup.find_all("tr")[1:]:
#    dataset = [td.get_text() for td in row.find_all("td")]
#    datasets.append(dataset)

#  print tables


  foundAlarmdepesche = {'Default':{},'Einsatzziel':{},'Transportziel':{}}
  operationTarget = {}
  transportDestination = {}

  isDefault = True
  isOperationTarget = False
  isTransportTarget = False


  for table in tables:
    (count, datasets) = table
    for dataset in datasets:
      availableAlarmdepesche = availableAlarmdepescheDefault
      identifier = "Default"
      # Einsatzziel
      if datasets[0][0].find("Einsatzziel") != -1:
        availableAlarmdepesche = availableAlarmdepescheOperationTarget
        identifier = "Einsatzziel"
      # Transportziel
      if datasets[0][0].find("Transportziel") != -1:
        availableAlarmdepesche = availableAlarmdepescheTransportTarget
        identifier = "Transportziel"

      for alarmdepItem in availableAlarmdepesche:
        if dataset[0].find(availableAlarmdepesche[alarmdepItem]) != -1 and len(dataset) > 1:
          item = dataset[1].encode('utf-8').rstrip()#dataset[1].decode("utf-8", 'ignore').rstrip()
          foundAlarmdepesche[identifier][alarmdepItem] = item

#  for dataset in datasets:
#    for alarmdepItem in availableAlarmdepesche:
#      item = dataset[1].encode('utf-8').rstrip()#dataset[1].decode("utf-8", 'ignore').rstrip()
##      if dataset[0] == availableAlarmdepesche[alarmdepItem]:
#      if dataset[0].find(availableAlarmdepesche[alarmdepItem]) != -1:
#        foundAlarmdepesche[alarmdepItem] = item 



  print foundAlarmdepesche

  return foundAlarmdepesche

def getDictValueByKey ( _key, _dict ):
  if _key in _dict:
    return _dict[_key]
  else:
    return ""

# TODO: 
def createSQLFromDict ( lastMailID, dicAlarmdepesche ):
  sqlQuery = "insert into Alarmdepesche (messageID, "
  # Default
  sqlQuery += "Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Name, Zusatz, Sachverhalt, Patientenname"
  # Einsatzziel
  sqlQuery += ", Target_Objekt, Target_Objekttyp, Target_StrasseHausnummer, Target_Segment, Target_PLZOrt, Target_Region, Target_Info"
  # TransportTarget
  sqlQuery += ", TransTarget_Transportziel, TransTarget_Objekt, TransTarget_Objekttyp, TransTarget_StrasseHausnummer, TransTarget_PLZOrt"
  sqlQuery += ") VALUES ("

  sqlQuery += str(lastMailID)+","
  # Default
  subDicAlarmdepesch = dicAlarmdepesche['Default'] if 'Default' in dicAlarmdepesche else {}
  sqlQuery += "\""+getDictValueByKey('Einsatzstichwort', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('AlarmiertesEinsatzmittel', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Sondersignal', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Einsatzbeginn', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Einsatznummer', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Name', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Zusatz', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Sachverhalt', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Patientenname', subDicAlarmdepesch)+"\","
  # Einsatzziel
  subDicAlarmdepesch = dicAlarmdepesche['Einsatzziel'] if 'Einsatzziel' in dicAlarmdepesche else {}
  sqlQuery += "\""+getDictValueByKey('Objekt', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Objekttyp', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('StrasseHausnummer', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Segment', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('PLZOrt', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Region', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Info', subDicAlarmdepesch)+"\","
  # TransportTarget
  subDicAlarmdepesch = dicAlarmdepesche['TransportTarget'] if 'TransportTarget' in dicAlarmdepesche else {}
#    subDicAlarmdepesch = dicAlarmdepesche['TransportTarget']
#  else:
#    subDicAlarmdepesch = {}
  sqlQuery += "\""+getDictValueByKey('Transportziel', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Objekt', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('Objekttyp', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('StrasseHausnummer', subDicAlarmdepesch)+"\","
  sqlQuery += "\""+getDictValueByKey('PLZOrt', subDicAlarmdepesch)+"\""


  # availableAlarmdepescheDefault: Sachverhalt, Sondersignal, Patientenname, 
  # availableAlarmdepescheTransportTarget: Transportziel, Objekt, Objekttyp, StrasseHausnummer, PLZOrt

  sqlQuery += ");"
  print (sqlQuery)

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

while True:
  runCheckup ()
  time.sleep(int(config.imap['checkIntervall']))

