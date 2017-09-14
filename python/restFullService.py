#!flask/bin/python
#-*-coding: utf-8 -*-
from flask import Flask, jsonify
import MySQLdb
import alarmdepescheconfig as config
import urllib

from flask_cors import CORS, cross_origin

import sys

reload(sys)
sys.getdefaultencoding()

print (sys.getfilesystemencoding())

app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'

#cors = CORS(app, resources={r"/api/v1.0/Alarmdepesche": {"origins": "http://127.0.0.1:5000"}})
cors = CORS(app, resources={r"/api/v1.0/Alarmdepesche": {"origins": "*"}})

#tasks = [
#    {
#        'id': 1,
#        'title': u'Buy groceries',
#        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
#        'done': False
#    },
#    {
#        'id': 2,
#        'title': u'Learn Python',
#        'description': u'Need to find a good Python tutorial on the web', 
#        'done': False
#    }
#]

def strEncode (_in):
  #return _in.decode("iso-8859-1").encode("utf-8") #.decode('utf-8', 'ignore')
  #return _in.decode("utf-8").encode("utf-8")
  return _in#.decode('utf-8', 'ignore')


@app.route('/api/v1.0/Alarmdepesche', methods=['GET'])
def get_tasks():
    db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'] )
    cursor = db.cursor()
    try:
      sqlStatement = "select id, dbIN, messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Target_Objekt, Target_Objekttyp, Target_StrasseHausnummer, Target_Segment, Target_PLZOrt, Target_Region, Target_Info, Name, Zusatz, TransTarget_Transportziel, TransTarget_Objekt, TransTarget_Objekttyp, TransTarget_StrasseHausnummer, TransTarget_PLZOrt from Alarmdepesche order by id desc limit 1";
      cursor.execute(sqlStatement)
      result = cursor.fetchone()
    except:
      print ("!Error in mysql statement")
      return jsonify({'Error':'Error in mysql statement'})
    db.close()

    #print urllib.quote(unicode(result[3], "utf-8")) # result[3].encode('ascii').encode('utf-8'))
    #test = result[3].decode('utf-8', 'ignore').strip().encode('utf-8')
    test = result[3].decode('utf-8', 'ignore')
    #print (urllib.quote(test))
    #print (type(test))

    alarmdepesche = { 'Default': { 'id'               : result[0]
                                 , 'dbIN'             : result[1]
                                 , 'messageID'        : result[2]
                                 , 'Einsatzstichwort' : strEncode(result[3])
                                 , 'AlarmiertesEinsatzmittel' : strEncode(result[4])
                                 , 'Sondersignal' : strEncode(result[5])
                                 , 'Einsatzbeginn' : strEncode(result[6])
                                 , 'Einsatznummer' : strEncode(result[7])
                                 , 'Name' : strEncode(result[15])
                                 , 'Zusatz' : strEncode(result[16])
                                 }
                    , 'Target' : { 'Objekt' : strEncode(result[8])
                                 , 'Objekttyp' : strEncode(result[9])
                                 , 'StrasseHausnummer' : strEncode(result[10])
                                 , 'Segment' : strEncode(result[11])
                                 , 'PLZOrt' : strEncode(result[12])
                                 , 'Region' : strEncode(result[13])
                                 , 'Info' : strEncode(result[14])
                                 }
                    , 'TransportTarget' : { 'Transportziel' : strEncode(result[17])
                                          , 'Objekt' : strEncode(result[18])
                                          , 'Objekttyp' : strEncode(result[19])
                                          , 'StrasseHausnummer' : strEncode(result[20])
                                          , 'PLZOrt' : strEncode(result[21])
                                          }
                      #, '' : result[]
                      }
    return jsonify( alarmdepesche)

#@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#def get_tasks():
#    return jsonify({'tasks': tasks})

#@app.route('/')
#def index():
#    return "Hello, World!"

if __name__ == '__main__':
    app.run(host= '0.0.0.0', threaded=True)
    #app.run(debug=True)
