#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gm <gm@PONTADATELHA>
#
# Distributed under terms of the MIT license.

"""

"""

import sys
from server import Server

class XMLServer(Server):
    def login(self, user, passwd):
        auth_result = Server.login(self, user, passwd)
        xmldata = []
        xmldata.append('<root>')
        xmldata.append('<status>ok</status>')
        if auth_result:
            xmldata.append('<authResult>0</authResult>')
        else:
            xmldata.append('<authResult>1</authResult>')
        xmldata.append('<forwardUrl>index.html</forwardUrl>')
        if not auth_result:
            xmldata.append('<errorMsg></errorMsg>')
        xmldata.append('</root>')
        return '\n'.join(xmldata)


    def getTemperatures(self):
        return reduce(lambda x,y: x+y, map(lambda sensor: ['<sensor>'] +
            ['<%s>%s</%s>' % (field,value,field) for field, value in
                sensor.iteritems()] + ['</sensor>'], Server.getTemperatures(self)))


    def getFans(self):
        return reduce(lambda x,y: x+y, map(lambda sensor: ['<sensor>'] +
            ['<%s>%s</%s>' % (field,value,field) for field, value in
                sensor.iteritems()] + ['</sensor>'], Server.getFans(self)))


    def getVoltages(self):
        return reduce(lambda x,y: x+y, map(lambda sensor: ['<sensor>'] +
            ['<%s>%s</%s>' % (field,value,field) for field, value in
                sensor.iteritems()] + ['</sensor>'], Server.getVoltages(self)))


    def get(self, field):
        xmldata = []
        xmldata.append('<root>')
        xmldata.append('<thresholdSensorList>')
        if field == 'temperatures':
            xmldata.extend(self.getTemperatures())
        elif field == 'fans':
            xmldata.extend(self.getFans())
        elif field == 'voltages':
            xmldata.extend(self.getVoltages())
        else:
            raise Exception('Field not implemented: ' + field)
        xmldata.append('</thresholdSensorList>')
        xmldata.append('<status>ok</status>')
        xmldata.append('</root>')
        return '\n'.join(xmldata)


if __name__ == '__main__':
    server = XMLServer(sys.argv[1])
    print server.get('temperatures')
    print
    print server.get('fans')
    print
    print server.get('voltages')
    print
    print server.login('lucio', 'namos')
    print
    print server.login('lala', 'lulu')
