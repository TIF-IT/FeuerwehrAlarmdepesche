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
        app.run(host='0.0.0.0', threaded=True)


    def strEncode(self, _in):
      return _in


    def get_tasks(self):
        db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'])
#        db = self.get_db_connection()
        cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        try:
            sqlStatement = "select id, dbIN, messageID, Patientenname, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Sachverhalt, Auftragsnummer, Einsatzbeginn, Einsatznummer, Target_Objekt, Target_Objekttyp, Target_StrasseHausnummer, Target_Segment, Target_Region, Target_Geopositionen, Target_PLZOrt, Target_Region, Target_Info, Name, Zusatz, TransTarget_Transportziel, TransTarget_Objekt, TransTarget_Objekttyp, TransTarget_StrasseHausnummer, TransTarget_PLZOrt, TransTarget_Segment, TransTarget_Region, TransTarget_Info, TransTarget_Geopositionen from Alarmdepesche order by id desc limit 1";
            cursor.execute(sqlStatement)
            result = cursor.fetchone()
            db.close()

        except:
            print ("!Error in mysql statement")
            return jsonify({'Error':'Error in mysql statement'})

        if not result:
            print('No entries found in db')
            return jsonify({'Error':'No entries found in db'}) 

        print (result)

        alarmdepesche = { 'Default': { 'id'               : result['id']
                                     , 'dbIN'             : str(result['dbIN'])
                                     , 'messageID'        : result['messageID']
                                     , 'Einsatzstichwort' : result['Einsatzstichwort']
                                     , 'AlarmiertesEinsatzmittel' : self.strEncode(result['AlarmiertesEinsatzmittel'])
                                     , 'Sondersignal' : self.strEncode(result['Sondersignal'])
                                     , 'Sachverhalt' : self.strEncode(result['Sachverhalt'])
                                     , 'Patientenname' : self.strEncode(result['Patientenname'])
                                     , 'Einsatzbeginn' : self.strEncode(result['Einsatzbeginn'])
                                     , 'Einsatznummer' : self.strEncode(result['Einsatznummer'])
                                     , 'Name' : self.strEncode(result['Name'])
                                     , 'Zusatz' : self.strEncode(result['Zusatz'])
                                     , 'Auftragsnummer' : self.strEncode(result['Auftragsnummer'])
                                     }
                        , 'Target' : { 'Objekt' : self.strEncode(result['Target_Objekt'])
                                     , 'Objekttyp' : self.strEncode(result['Target_Objekttyp'])
                                     , 'StrasseHausnummer' : self.strEncode(result['Target_StrasseHausnummer'])
                                     , 'Segment' : self.strEncode(result['Target_Segment'])
                                     , 'PLZOrt' : self.strEncode(result['Target_PLZOrt'])
                                     , 'Region' : self.strEncode(result['Target_Region'])
                                     , 'Info' : self.strEncode(result['Target_Info'])
                                     , 'Geopositionen' : self.strEncode(result['Target_Geopositionen'])
                                     }
                        , 'TransportTarget' : { 'Transportziel' : self.strEncode(result['TransTarget_Transportziel'])
                                              , 'Objekt' : self.strEncode(result['TransTarget_Objekt'])
                                              , 'Objekttyp' : self.strEncode(result['TransTarget_Objekttyp'])
                                              , 'StrasseHausnummer' : self.strEncode(result['TransTarget_StrasseHausnummer'])
                                              , 'PLZOrt' : self.strEncode(result['TransTarget_PLZOrt'])
                                              , 'Region' : self.strEncode(result['TransTarget_Region'])
                                              , 'Info' : self.strEncode(result['TransTarget_Info'])
                                              , 'Segment' : self.strEncode(result['TransTarget_Segment'])
                                              , 'Geopositionen' : self.strEncode(result['TransTarget_Geopositionen'])
                                              }
                        }

        return json.dumps(alarmdepesche, ensure_ascii=False)

