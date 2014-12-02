
BMC Dummy
=========

This project simulates the behavior of a server's BMC board, responsible for
sensor readings and power management, among other features. Current
implementation mimics the basic BMC functionality of Lenovo servers (power
management and temperature, fan and voltage sensor data). Data isgenerated in
XML format and connections are performed through an HTTP REST interface.


Running
=======

``$ python main.py [-h] [-p PORT] [--sensordata SENSORDATA]``

Will execute the XMLServer implementation with sensor setup as provided in
server/sensor\_data.csv. Optional port argument sets the port on which the
server will listen to requests, defaults to 8080. Optional sensordata argument
refers to the csv file containing the server's sensor settings, defaults to
'server/sensor\_data.csv'.

