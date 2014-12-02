#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Main script. Executes the XML Server implementation with an HTTP
    connection and default parameters.
"""

import sys
from server import xml_server
from connection import http_connection

if __name__ == '__main__':
    server = xml_server.XMLServer('server/sensor_data.csv')
    if len(sys.argv) == 1:
        connection = http_connection.HttpConnection(server)
    elif len(sys.argv) == 2:
        port = int(sys.argv[1])
        connection = http_connection.HttpConnection(server, port=port)
    else:
        sys.exit(1)
