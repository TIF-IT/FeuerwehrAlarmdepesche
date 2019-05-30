#!/usr/bin/python
# -*- coding: utf-8 -*-

from Alarmdepesche.registry import ModuleRegistry
import Alarmdepesche.alarmdepescheconfig as config
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


    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()


    def register_to_input(self, f):
        print('register input for %s' % f)
        self.on_input_list.append(f)


    def get_db_connection(self):
        return self.db


    def get_instance(self, module_class):
        for x in self.modules:
            if x.__class__ is module_class:
                return x
        return None

    def new_alarm(self, sender=None, message_id=0, dicAlarmdepesche=None):
        for i in self.on_input_list:
            if i.__self__ is sender:
                continue
            i(message_id, dicAlarmdepesche)



