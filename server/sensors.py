#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gm <gm@PONTADATELHA>
#
# Distributed under terms of the MIT license.

"""

"""

import random

class Sensor(object):
    def __init__(self, name, units='', val_format='%.5f',
            lowerNC=None, upperNC=None, lowerCT=None, upperCT=None,
            lowerNR=None, upperNR=None, mu=0, sigma=1):
        self.status = 'Normal'
        self.name = name
        self.units = units
        self.__value_fmt = val_format
        self.reading = None
        self.non_critical = (lowerNC, upperNC)
        self.critical = (lowerCT, upperCT)
        self.non_recoverable = (lowerNR, upperNR)
        self.__mu = mu
        self.__sigma = sigma
        self.update()

    def __format(self, data):
        ''' formats data according to sensor data format '''
        if data:
            return self.value_fmt % data
        return 'N/A'

    def update(self):
        ''' update sensor reading '''
        self.reading = random.gauss(self.__mu, self.__sigma)

    def repr(self):
        ''' generate sensor representation '''
        sensor = {}
        sensor['name'] = self.name
        sensor['status'] = self.status
        sensor['units'] = self.units
        sensor['reading'] = self.__format(self.reading)
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

