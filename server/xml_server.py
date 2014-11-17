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
        auth_result = Server.login(self, user, passwd)
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


if __name__ == '__main__':
    server = XMLServer(sys.argv[1])
    print ET.tostring(server.getSensors('temperatures'))
    print
    print ET.tostring(server.getSensors('fans'))
    print
    print ET.tostring(server.getSensors('voltages'))
    print
    print server.login('lucio', 'namos')
    print
    print server.login('lala', 'lulu')
