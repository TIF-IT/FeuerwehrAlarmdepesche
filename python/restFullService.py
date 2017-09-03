#!flask/bin/python
from flask import Flask, jsonify
import MySQLdb
import alarmdepescheconfig as config
import urllib

from flask.ext.cors import CORS, cross_origin

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

@app.route('/api/v1.0/Alarmdepesche', methods=['GET'])
def get_tasks():
    db = MySQLdb.connect(config.mysql['host'], config.mysql['user'], config.mysql['passwd'], config.mysql['dbName'] )
    cursor = db.cursor()
    try:
      sqlStatement = "select id, dbIN, messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Objekt, Objekttyp, StrasseHausnummer, Segment, PLZOrt, Region, Info, Name, Zusatz from Alarmdepesche order by id desc limit 1";
      cursor.execute(sqlStatement)
      result = cursor.fetchone()
    except:
      print ("!Error in mysql statement")
      return jsonify({'Alarmdepesche': {'Error':'Error in mysql statement'}})
    db.close()

    #print urllib.quote(unicode(result[3], "utf-8")) # result[3].encode('ascii').encode('utf-8'))
    #test = result[3].decode('utf-8', 'ignore').strip().encode('utf-8')
    test = result[3].decode('utf-8', 'ignore')
    print (urllib.quote(test))

    alarmdepesche = { 'id'               : result[0]
                    , 'dbIN'             : result[1]
                    , 'messageID'        : result[2]
                    , 'Einsatzstichwort' : test
                      #, 'AlarmiertesEinsatzmittel' : result[4]
                      #, 'Sondersignal' : result[5]
                      #, 'Einsatzbeginn' : result[6]
                      #, 'Einsatznummer' : result[7]
                      #, 'Objekt' : result[8]
                      #, 'Objekttyp' : result[9]
                      #, 'StrasseHausnummer' : result[10]
                      #, 'Segment' : result[11]
                      #, 'PLZOrt' : result[12]
                      #, 'Region' : result[13]
                      #, 'Info' : result[14]
                      #, 'Name' : result[15]
                      #, 'Zusatz' : result[16]
#id, dbIN, messageID, Einsatzstichwort, AlarmiertesEinsatzmittel, Sondersignal, Einsatzbeginn, Einsatznummer, Objekt, Objekttyp, StrasseHausnummer, Segment, PLZOrt, Region, Info, Name, Zusatz
                      #, '' : result[]
                      }
    return jsonify({'Alarmdepesche': alarmdepesche})

#@app.route('/todo/api/v1.0/tasks', methods=['GET'])
#def get_tasks():
#    return jsonify({'tasks': tasks})

#@app.route('/')
#def index():
#    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
