#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Base Server implementation. Must be specialized for custom data formats.
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
        self.__rebootCount = 0
        self.__sensorTypes = ['temperatures', 'fans', 'voltages']
        self.init_sensors(sensor_data_file)


    def init_sensors(self, sensor_data_file):
        """ Creates all server's sensors from data contained in the CSV on
            sensor_data_file. CSV format must be as follows (fields with * are
            optional):
                type (currently [temperature|fan|voltage])
                name
                *lower non-recoverable bound
                *lower critical bound
                *lower non-critical bound
                *upper non-critical bound
                *upper critical bound
                *upper non-recoverable bound
        """
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
        """ Validates provided user and password values according to the ones
            set on creation.
        """
        if user == self.__user and passwd == self.__passwd:
            return True
        return False


    def getTemperatures(self):
        """ Generates data from all temperature sensors. """
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__temperatures)
        self.__rebootPause()


    def getFans(self):
        """ Generates data from all fan sensors. """
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__fans)
        self.__rebootPause()


    def getVoltages(self):
        """ Generates data from all voltage sensors. """
        if self.__pwState == ON:
            return map(lambda x: x.data(), self.__voltages)
        self.__rebootPause()


    def getPwState(self):
        """ Generates power state data. """
        self.__rebootPause()
        return str(self.__pwState)


    def setPwState(self, state):
        """ Alter server's power state. """
        if state not in (OFF, ON, RESET, HARD_RESET):
            raise Exception('Unrecognized state: ' + state)
        if state in (RESET, HARD_RESET):
            if self.__pwState == OFF:
                return False
            elif self.__pwState == ON:
                self.__pwState = OFF
                self.__rebootCount = 4 if state == RESET else 8
                return True
        if state == OFF and self.__pwState == ON:
            self.__pwState = OFF
        if state == ON and self.__pwState == OFF:
            self.__pwState = ON
        return True


    def __rebootPause(self):
        """ Simulates the time needed for server reboot. Currently, a normal
            reset will keep the server off for the next 4 "get" method calls,
            and a hard reset, 8.
        """
        if self.__rebootCount:
            self.__rebootCount -= 1
            if self.__rebootCount == 0:
                self.__pwState = ON


if __name__ == '__main__':
    server = Server(sys.argv[1])
    print server.getTemperatures()
    print server.getFans()
    print server.getVoltages()
