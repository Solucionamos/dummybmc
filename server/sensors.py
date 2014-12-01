#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Implements a standard Sensor class, and a few specializations which consist
    of pre-set values for some attributes.
"""

import random
from collections import OrderedDict

def _in(value, interval):
    """ checks if a float value lies within an interval. Interval bounds
        may be float numbers represented as strings, or None.
    """
    lower, upper = map(lambda v: v and float(v), interval)
    if lower and value < lower:
        return False
    if upper and upper < value:
        return False
    return True


class Sensor(object):
    """ Base Sensor implementation. Must have a name set on creation.
        Optional lower and upper bounds for non-critical (NC), critical (CT)
        and non-recoverable (NR) values may be provided, and if present will
        be used to shape the value distribution of sensor data.
    """
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

        """ low and high determine the shape of the normal distribution used
            for sensor reading update. It will be centered on the average of
            the two values, and the distance between the average and the bounds
            will be 3 standard deviations, causing ~99.7% of generated readings
            to fall within the bounds.
        """

        self.__mu = (low + high) / 2
        self.__sigma = (high - self.__mu) / 3
        self.update()


    def __format(self, data):
        """ Formats data according to sensor data format """
        if data:
            return self.__value_fmt % float(data)
        return 'N/A'


    def update(self):
        """ Updates sensor reading. Employs a normal distribution taking into
            account the sensor's value bounds.
        """
        self.reading = random.gauss(self.__mu, self.__sigma)
        if not _in(self.reading, self.non_recoverable):
            # something terrible happened, we don't know what a true server
            # would use as status in this case...
            self.status = 'Catastrophe'
        elif not _in(self.reading, self.critical):
            self.status = 'Critical'
        elif not _in(self.reading, self.non_critical):
            self.status = 'Warning'
        else:
            self.status = 'Normal'


    def data(self):
        """ Generates sensor representation, as an Ordered Dict. """
        self.update() # Updates sensor data before new reading
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
    """ Temperature sensor has integer readings and limits. Value unit is
        degrees Celsius.
    """
    def __init__(self, name, **limits):
        Sensor.__init__(self, name, units='C', val_format='%d',
                _low=0, _high=100, **limits)


class FanSensor(Sensor):
    """ Fan sensor has integer readings and limits. Value unit is RPM. """
    def __init__(self, name, **limits):
        Sensor.__init__(self, name, units='RPM', val_format='%d',
                _low=10, _high=5000, **limits)


class VoltageSensor(Sensor):
    """ Voltage sensor has float readings and limits, with 5 decimal digits of
        precision. Value unit is Volts.
    """
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
    while volt2.status != 'Critical':
        print volt2.data()
