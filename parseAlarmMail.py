#!/usr/bin/python3

import imaplib
import socket
import ssl
from HTMLParser import HTMLParser
from email.parser import FeedParser
import alarmdepescheconfig as config

# https://stackoverflow.com/questions/25318012/how-to-connect-with-python-imap4-ssl-and-self-signed-server-ssl-cert

ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  
#passwd = getpass.getpass()
mail =  imaplib.IMAP4_SSL(config.imap['host'], config.imap['port'])
mail.login(config.imap['user'], config.imap['passwd'])
mail.select(config.imap['mailBox'], 1)

result, data = mail.search(None, "ALL")
 
ids = data[0] # data is a list.
id_list = ids.split() # ids is a space separated string
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

# =====================================================

#parsed_html = BeautifulSoup(html)
#print parsed_html.body.find('div', attrs={'class':'container'}).text

from bs4 import BeautifulSoup

soup = BeautifulSoup(mailBody, "lxml")
table = soup.find("table", attrs={})

# The first tr contains the field names.
#headings = [th.get_text() for th in table.find("tr").find_all("th")]

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
#                         , '':''
                         }

foundAlarmdepesche = {}

for dataset in datasets:
  for alarmdepItem in availableAlarmdepesche:
    if dataset[0] == availableAlarmdepesche[alarmdepItem]:
      foundAlarmdepesche[alarmdepItem] = dataset[1]

print foundAlarmdepesche


sqlQuery = "insert into Alarmdepesche (messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Objekt, Objekttyp, StrasseHausnummer, Segment, PLZOrt, Region, Info, Name, Zusatz) VALUES ("

sqlQuery += str(latest_email_id)+","
sqlQuery += "\""+foundAlarmdepesche["Einsatzstichwort"]+"\","
sqlQuery += "\""+foundAlarmdepesche["AlarmiertesEinsatzmittel"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Sondersignal"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Einsatzbeginn"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Einsatznummer"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Objekt"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Objekttyp"]+"\","
sqlQuery += "\""+foundAlarmdepesche["StrasseHausnummer"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Segment"]+"\","
sqlQuery += "\""+foundAlarmdepesche["PLZOrt"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Region"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Info"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Name"]+"\","
sqlQuery += "\""+foundAlarmdepesche["Zusatz"]+"\""

#sqlQuery += "\""+foundAlarmdepesche[""]+"\","


sqlQuery += ");"

print ("> "+sqlQuery)

