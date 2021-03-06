#!/usr/bin/python
# -*- coding: utf-8 -*-


class Api:
    def __init__(self, core):
        print('install core %s on %s' % (core, self))
        self.__core = core


    def config(self):
        pass


    def get_db_connection(self):
        return self.__core.get_db_connection()


    def register_to_input(self, f):
        self.__core.register_to_input(f)


    def new_alarm(self, message_id, dicAlarmdepesche):
        print('i am %s' % self)
        self.__core.new_alarm(sender=self,
                              message_id=message_id,
                              dicAlarmdepesche=dicAlarmdepesche)


class ModuleRegistry:
    _objs = []
    # [(extensionTyp,extensionFunction)] 
    _extensions = [] 

    def register(c):
        try:
            assert issubclass(c, Api)
            ModuleRegistry._objs.append(c)
        except AssertionError:
            print('Subcalss {} from Api to register as module'.format(c.__name__))
        return c


    def get_objects():
        return ModuleRegistry._objs

    def callExtensionPoints(extensionTyp, obj):
        extensionObject = obj
        for (extensionTyp, extensionFunction) in ModuleRegistry._extensions:
            if extensionTyp == extensionTyp:
              print ("Call extension point for typ "+extensionTyp)
              extensionObject = extensionFunction(extensionObject)
        return extensionObject

    def registerExtensionPoint(extensionTyp, extensionFunction):
        ModuleRegistry._extensions.append((extensionTyp, extensionFunction))


