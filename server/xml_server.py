#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Server implementation that generates data in XML format. Employs the
    ElementTree module for XML generation.
"""

import sys
import xml.etree.ElementTree as ET
from server import Server

def add_subelement(parent, name, text=' '):
    """ Helper function. Adds a subelement with a given name and an optional
        text to a parent element.
    """
    subelement = ET.SubElement(parent, name)
    subelement.text = text
    return subelement


class XMLServer(Server):
    def login(self, user, passwd):
        """ Authenticates the provided user and password, and generates the
            login response.
        """
        auth_result = Server.check_login(self, user, passwd)
        root = ET.Element('root')
        add_subelement(root, 'status', 'ok')
        add_subelement(root, 'authResult', '0' if auth_result else '1')
        add_subelement(root, 'forwardUrl', 'index.html')
        if not auth_result:
            add_subelement(root, 'errorMsg')
        return ET.tostring(root)


    def getSensors(self, sensor_type):
        """ Wrapper method that generates XML for requests of sensor data.
            Outputs data from all the sensors of given sensor_type.
        """
        sensors = ET.Element('thresholdSensorList')

        if sensor_type == 'temperatures':
            sensor_data = Server.getTemperatures(self)
        elif sensor_type == 'fans':
            sensor_data = Server.getFans(self)
        elif sensor_type == 'voltages':
            sensor_data = Server.getVoltages(self)
        else:
            raise Exception('Field not implemented: ' + field)

        if not sensor_data:
            return None

        for sensor_dict in sensor_data:
            sensor = ET.SubElement(sensors, 'sensor')
            [add_subelement(sensor, field, value) for field, value
                    in sensor_dict.iteritems()]

        return sensors


    def getPwState(self):
        """ Wrapper method for power state requests. """
        pwState = ET.Element('pwState')
        pwState.text = Server.getPwState(self)
        return pwState


    def get(self, parameter):
        """ Main method for get requests. Builds XML root and calls the
            appropriate wrapper method for its content.
        """
        root = ET.Element('root')
        if parameter == 'pwState':
            root.append(self.getPwState())
        elif parameter in self._Server__sensorTypes:
            sensor_data = self.getSensors(parameter)
            if sensor_data:
                root.append(sensor_data)
        else:
            raise Exception('Unrecognized parameter: ' + parameter)
        add_subelement(root, 'status', 'ok')
        return ET.tostring(root)


    def setPwState(self, state):
        """ Main power management method. Alters the server's power state. """
        root = ET.Element('root')
        if Server.setPwState(self, state):
            add_subelement(root, 'status', 'ok')
        else:
            add_subelement(root, 'status', 'ProcessingError')
            add_subelement(root, 'errorMsg', 'Error while setting new values.')
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
    print
    print server.setPwState(0)
    print
    print server.get('pwState')
    print
    print server.get('temperatures')
    print
    print server.setPwState(3)
    print
    print server.get('pwState')
