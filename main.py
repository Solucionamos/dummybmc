#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Main script. Executes the XML Server implementation with an HTTP
    connection and default parameters.
"""

from server import xml_server
from connection import http_connection

if __name__ == '__main__':
    server = xml_server.XMLServer('server/sensor_data.csv')
    connection = http_connection.HttpConnection(server)
