#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.registry import ModuleRegistry, Api

import MySQLdb
import Alarmdepesche.alarmdepescheconfig as config
import urllib
import json
import sys
import _thread

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/api/v1.0/Alarmdepesche": {"origins": "*"}})

@ModuleRegistry.register
class HtmlModule(Api):

    def config(self):
        app.add_url_rule('/api/v1.0/Alarmdepesche', methods=['GET'], view_func=self.get_tasks)
        _thread.start_new_thread(app.run, tuple(), {'host': '0.0.0.0', 'threaded': True})


    def strEncode(self, _in):
      return _in


    def get_tasks(self):
        db = self.get_db_connection()
        cursor = db.cursor()
        try:
            sqlStatement = "select id, dbIN, messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Target_Objekt, Target_Objekttyp, Target_StrasseHausnummer, Target_Segment, Target_PLZOrt, Target_Region, Target_Info, Name, Zusatz, TransTarget_Transportziel, TransTarget_Objekt, TransTarget_Objekttyp, TransTarget_StrasseHausnummer, TransTarget_PLZOrt from Alarmdepesche order by id desc limit 1";
            cursor.execute(sqlStatement)
            result = cursor.fetchone()
        except:
            print ("!Error in mysql statement")
            return jsonify({'Error':'Error in mysql statement'})

        if not result:
            print('No entries found in db')
            return ''

        alarmdepesche = { 'Default': { 'id'               : result[0]
                                     , 'dbIN'             : str(result[1])
                                     , 'messageID'        : result[2]
                                     , 'Einsatzstichwort' : result[3]
                                     , 'AlarmiertesEinsatzmittel' : self.strEncode(result[4])
                                     , 'Sondersignal' : self.strEncode(result[5])
                                     , 'Einsatzbeginn' : self.strEncode(result[6])
                                     , 'Einsatznummer' : self.strEncode(result[7])
                                     , 'Name' : self.strEncode(result[15])
                                     , 'Zusatz' : self.strEncode(result[16])
                                     }
                        , 'Target' : { 'Objekt' : self.strEncode(result[8])
                                     , 'Objekttyp' : self.strEncode(result[9])
                                     , 'StrasseHausnummer' : self.strEncode(result[10])
                                     , 'Segment' : self.strEncode(result[11])
                                     , 'PLZOrt' : self.strEncode(result[12])
                                     , 'Region' : self.strEncode(result[13])
                                     , 'Info' : self.strEncode(result[14])
                                     }
                        , 'TransportTarget' : { 'Transportziel' : self.strEncode(result[17])
                                              , 'Objekt' : self.strEncode(result[18])
                                              , 'Objekttyp' : self.strEncode(result[19])
                                              , 'StrasseHausnummer' : self.strEncode(result[20])
                                              , 'PLZOrt' : self.strEncode(result[21])
                                              }
                        }

        return json.dumps(alarmdepesche, ensure_ascii=False)

