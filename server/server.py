#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gm <gm@PONTADATELHA>
#
# Distributed under terms of the MIT license.

"""

"""

import sys, csv
import sensors

# Power states
OFF = 0
ON = 1
RESET = 2
HARD_RESET = 3

class Server(object):
    def __init__(self, sensor_data_file, user='lucio', passwd='namos'):
        self.__user = user
        self.__passwd = passwd
        self.__temperatures = []
        self.__fans = []
        self.__voltages = []
        self.__pwState = ON
        self.__sensorTypes = ['temperatures', 'fans', 'voltages']
        self.init_sensors(sensor_data_file)


    def init_sensors(self, sensor_data_file):
        with open(sensor_data_file, 'r') as sensor_data:
            reader = csv.DictReader(sensor_data, ['type', 'name', 'lowerNR',
                'lowerCT', 'lowerNC', 'upperNC', 'upperCT', 'upperNR'])
            for sensor in reader:
                sensor_type = sensor.pop('type')
                if sensor_type == 'temperature':
                    self.__temperatures.append(
                            sensors.TemperatureSensor(**sensor))
                elif sensor_type == 'fan':
                    self.__fans.append(
                            sensors.FanSensor(**sensor))
                elif sensor_type == 'voltage':
                    self.__voltages.append(
                            sensors.VoltageSensor(**sensor))
                else:
                    raise Exception('Unrecognized sensor type: ' + sensor_type)


    def check_login(self, user, passwd):
        if user == self.__user and passwd == self.__passwd:
            return True
        return False


    def getTemperatures(self):
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__temperatures)


    def getFans(self):
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__fans)


    def getVoltages(self):
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__voltages)


    def getPwState(self):
        return str(self.__pwState)


if __name__ == '__main__':
    server = Server(sys.argv[1])
    print server.getTemperatures()
    print server.getFans()
    print server.getVoltages()
