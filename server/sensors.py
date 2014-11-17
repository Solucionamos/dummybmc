#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

import random
from collections import OrderedDict

class Sensor(object):
    def __init__(self, name, units='', val_format='%.5f',
            lowerNC=None, upperNC=None, lowerCT=None, upperCT=None,
            lowerNR=None, upperNR=None, _low=0, _high=10):
        self.status = 'Normal'
        self.name = name
        self.units = units
        self.__value_fmt = val_format
        self.reading = None
        self.non_critical = (lowerNC, upperNC)
        self.critical = (lowerCT, upperCT)
        self.non_recoverable = (lowerNR, upperNR)

        if lowerNR:
            low = float(lowerNR)
        elif lowerCT:
            low = float(lowerCT) / 1.1
        elif lowerNC:
            low = float(lowerNC) / 1.3
        else:
            low = float(_low)

        if upperNR:
            high = float(upperNR)
        elif upperCT:
            high = float(upperCT) * 1.1
        elif upperNC:
            high = float(upperNC) * 1.3
        else:
            high = float(_high)

        self.__mu = (low + high) / 2
        self.__sigma = (high - self.__mu) / 3
        self.update()


    def __format(self, data):
        ''' formats data according to sensor data format '''
        if data:
            return self.__value_fmt % float(data)
        return 'N/A'


    def update(self):
        ''' update sensor reading '''
        self.reading = random.gauss(self.__mu, self.__sigma)


    def data(self):
        ''' generate sensor representation '''
        sensor = OrderedDict()
        sensor['sensorStatus'] = self.status
        sensor['name'] = self.name
        sensor['reading'] = self.__format(self.reading)
        sensor['units'] = self.units
        lower, upper = self.non_critical
        sensor['lowerNC'] = self.__format(lower)
        sensor['upperNC'] = self.__format(upper)
        lower, upper = self.critical
        sensor['lowerCT'] = self.__format(lower)
        sensor['upperCT'] = self.__format(upper)
        lower, upper = self.non_recoverable
        sensor['lowerNR'] = self.__format(lower)
        sensor['upperNR'] = self.__format(upper)
        return sensor


class TemperatureSensor(Sensor):
    def __init__(self, name, **limits):
        Sensor.__init__(self, name, units='C', val_format='%d',
                _low=0, _high=100, **limits)


class FanSensor(Sensor):
    def __init__(self, name, **limits):
        Sensor.__init__(self, name, units='RPM', val_format='%d',
                _low=10, _high=5000, **limits)


class VoltageSensor(Sensor):
    def __init__(self, name, **limits):
        Sensor.__init__(self, name, units='V', val_format='%.5f',
                _low=0, _high=10, **limits)


if __name__ == '__main__':
    temp1 = TemperatureSensor('temp1')
    print temp1.data()
    temp2 = TemperatureSensor('temp2', lowerCT=100, upperCT=1000)
    print temp2.data()
    fan1 = FanSensor('fan1')
    print fan1.data()
    fan2 = FanSensor('fan2', lowerCT=-200, upperCT=-100)
    print fan2.data()
    volt1 = VoltageSensor('volt1')
    print volt1.data()
    volt2 = VoltageSensor('volt2', lowerCT=4, upperCT=6)
    print volt2.data()
