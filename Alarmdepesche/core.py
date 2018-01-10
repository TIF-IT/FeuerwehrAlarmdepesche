#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.registry import ModuleRegistry
import imaplib
import socket
try:
  from HTMLParser import HTMLParser
except ModuleNotFoundError as e:
  from html.parser import HTMLParser
from email.parser import FeedParser
import Alarmdepesche.alarmdepescheconfig as config
from bs4 import BeautifulSoup
import MySQLdb
import time
import _thread

class Core:
    def __init__(self):
        self.modules = []
        self.on_input_list = []
        self.on_output_list = []
        try:
            self.db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'] )
        except Exception as e:
            print(e)
            raise Exception("Error at connecting to database")
        print('create modules %s' % ModuleRegistry.get_objects())
        for o in ModuleRegistry.get_objects():
            n = o(self)
            print('create %s' % n)
            _thread.start_new_thread(n.config, tuple())
            self.modules.append(n)
        for o in self.modules:
            o.write_to_db()


    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()


    def register_to_input(self, f):
        self.on_input_list.append(f)


    def get_db_connection(self):
        return self.db


    def get_instance(self, module_class):
        for x in self.modules:
            if x.__class__ is module_class:
                return x
        return None

    def new_alarm(self, sender=None, message_id=0, dicAlarmdepesche=None):
        sqlAlarmdepesche = self.createSQLFromDict(message_id, dicAlarmdepesche)
        self.insertAlarmdepescheIntoDB(dicAlarmdepesche, sqlAlarmdepesche)
        for i in self.on_input_list:
            if i.__self__ is sender:
                continue
            i(message_id, dicAlarmdepesche)


    def createSQLFromDict(self, lastMailID, dicAlarmdepesche):
      sqlQuery = ""
      names_list = ["Default", "Einsatzziel", "Transportziel"]
      target_pre = "Target_"
      trans_pre  = "TransTarget_"
      default    = ["Einsatzstichwort",
                    "AlarmiertesEinsatzmittel",
                    "Sondersignal",
                    "Einsatzbeginn",
                    "Einsatznummer",
                    "Name",
                    "Zusatz",
                    "Sachverhalt",
                    "Patientenname"]
      target     = ["Objekt",
                    "Objekttyp",
                    "StrasseHausnummer",
                    "Segment",
                    "PLZOrt",
                    "Region",
                    "Info"]
      trans      = ["Transportziel",
                    "Objekt",
                    "Objekttyp",
                    "StrasseHausnummer",
                    "PLZOrt"]
      combined   = { names_list[0] : default,
                     names_list[1] : target,
                     names_list[2] : trans}

      names  = ['messageID']
      names += default
      names += [target_pre + x for x in  target]
      names += [trans_pre + x for x in trans]

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


    def insertAlarmdepescheIntoDB(self, dicAlarmdepesche, sqlAlarmdepesche):
      # config.mysql['host'] , user, passwd, dbName
      # https://www.tutorialspoint.com/python/python_database_access.htm
      cursor = self.db.cursor()
      try:
        subDicAlarmdepesch = dicAlarmdepesche['Default'] if 'Default' in dicAlarmdepesche else {"Einsatznummer":0}
        sqlStatement = "select id from Alarmdepesche where Einsatznummer='"+subDicAlarmdepesch["Einsatznummer"]+"';"
        cursor.execute(sqlStatement)
        results = cursor.fetchall()
      except Exception as e:
        print(e)
        print ("!Error in select sql statement")
      try:
        # print results
        row_count = cursor.rowcount
        if row_count == 0:
          print ("Found new Alarmdepesche")
          # print (sqlAlarmdepesche) #.decode('utf-8', 'ignore'))
          cursor.execute(sqlAlarmdepesche)
          self.db.commit()
        else:
          print ("The Alarmdepesche is already existing")
      except Exception as e:  # TODO: catch only DB exception
        print(e)
        print ("!Error in mysql statement")
        self.db.rollback()

