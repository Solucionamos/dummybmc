#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Main script. Executes the XML Server implementation with an HTTP
    connection and default parameters.
"""

import sys
import argparse
from server import xml_server, defective_servers
from connection import http_connection

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=8080,
        help="server's HTTP port")
parser.add_argument('--sensordata', type=str,
        default='server/sensor_data.csv', help="sensor data file")
parser.add_argument('--randomloss', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.randomloss:
        server = defective_servers.RandomLossXMLServer(args.sensordata)
    else:
        server = xml_server.XMLServer(args.sensordata)
    connection = http_connection.HttpConnection(server, port=args.port)
