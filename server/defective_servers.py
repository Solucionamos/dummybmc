#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

""" Defective XML Server in which every message character has LOSS_PROB chance
    to be lost.
"""

import random
from xml_server import XMLServer

LOSS_PROB = 1.0/100

def random_loss(message):
    return ''.join(map(lambda x: x if random.random() > LOSS_PROB else '',
        message))

class RandomLossXMLServer(XMLServer):
    def login(self, user, passwd):
        return random_loss(XMLServer.login(self, user, passwd))

    def get(self, parameter):
        return random_loss(XMLServer.get(self, parameter))

    def setPwState(self, state):
        return random_loss(XMLServer.setPwState(self, state))


