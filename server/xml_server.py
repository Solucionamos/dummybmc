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
import xml.etree.ElementTree as ET
from server import Server

def add_subelement(parent, name, text=' '):
    subelement = ET.SubElement(parent, name)
    subelement.text = text
    return subelement


class XMLServer(Server):
    def login(self, user, passwd):
        auth_result = Server.check_login(self, user, passwd)
        root = ET.Element('root')
        add_subelement(root, 'status', 'ok')
        add_subelement(root, 'authResult', '0' if auth_result else '1')
        add_subelement(root, 'forwardUrl', 'index.html')
        if not auth_result:
            add_subelement(root, 'errorMsg')
        return ET.tostring(root)


    def getSensors(self, sensor_type):
        sensors = ET.Element('thresholdSensorList')

        if sensor_type == 'temperatures':
            sensor_data = Server.getTemperatures(self)
        elif sensor_type == 'fans':
            sensor_data = Server.getFans(self)
        elif sensor_type == 'voltages':
            sensor_data = Server.getVoltages(self)
        else:
            raise Exception('Field not implemented: ' + field)

        for sensor_dict in sensor_data:
            sensor = ET.SubElement(sensors, 'sensor')
            [add_subelement(sensor, field, value) for field, value
                    in sensor_dict.iteritems()]

        return sensors


    def getPwState(self):
        pwState = ET.Element('pwState')
        pwState.text = Server.getPwState(self)
        return pwState


    def get(self, parameter):
        root = ET.Element('root')
        if parameter == 'pwState':
            root.append(self.getPwState())
        elif parameter in self._Server__sensorTypes:
            root.append(self.getSensors(parameter))
        else:
            raise Exception('Unrecognized parameter: ' + parameter)
        add_subelement(root, 'status', 'ok')
        return ET.tostring(root)


if __name__ == '__main__':
    server = XMLServer(sys.argv[1])
    print server.get('temperatures')
    print
    print server.get('fans')
    print
    print server.get('voltages')
    print
    print server.get('pwState')
    print
    print server.login('lucio', 'namos')
    print
    print server.login('lala', 'lulu')
