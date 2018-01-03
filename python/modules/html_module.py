#!/usr/bin/python
# -*- coding: utf-8 -*-

from registry import ModuleRegistry, Api

import MySQLdb
import alarmdepescheconfig as config
import urllib
import json
import _thread

from http.server import BaseHTTPRequestHandler, HTTPServer

import sys


@ModuleRegistry.register
class HtmlModule(BaseHTTPRequestHandler, Api):
    instance = None

    def __init__(self, *argv):
        if len(argv) == 1:
            if not HtmlModule.instance:
                Api.__init__(self, *argv)
                HtmlModule.instance = self
            else:
                Api.__init__(HtmlModule.instance, *argv)
        else:
            if not HtmlModule.instance:
                BaseHTTPRequestHandler.__init__(self, *argv)
                HtmlModule.instance = self
            else:
                BaseHTTPRequestHandler.__init__(HtmlModule.instance, *argv)


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


    def do_GET(self):
        self._set_headers()
        self.wfile.write(str.encode(self.get_tasks()))


    def strEncode (self, _in):
        return _in


    def config(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, HtmlModule)
        _thread.start_new_thread(httpd.serve_forever, (None,))


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

