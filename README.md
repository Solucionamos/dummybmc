
BMC Dummy
=========

This project simulates the behavior of a server's BMC board, responsible for
sensor readings and power management, among other features. Current
implementation mimics the basic BMC functionality of Lenovo servers (power
management and temperature, fan and voltage sensor data). Data isgenerated in
XML format and connections are performed through an HTTP REST interface.


Running
=======

``$ python main.py``

Will execute the XMLServer implementation with sensor setup as provided in
server/sensor\_data.csv.

