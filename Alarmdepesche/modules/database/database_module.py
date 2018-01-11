#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.registry import ModuleRegistry, Api
import Alarmdepesche.alarmdepescheconfig as config


@ModuleRegistry.register
class DBModule(Api):
    def config(self):
        self.register_to_input(self.on_new_alarm)


    def on_new_alarm(self, message_id, dicAlarmdepesche):
        sqlAlarmdepesche = self.createSQLFromDict(message_id, dicAlarmdepesche)
        self.insertAlarmdepescheIntoDB(dicAlarmdepesche, sqlAlarmdepesche)


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
