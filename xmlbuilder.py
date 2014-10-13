#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 gm <gm@PONTADATELHA>
#
# Distributed under terms of the MIT license.

"""

"""

import bmcdata

HEAD = '_head'
ROOT = '_root'
STATUS = '_status'
TAIL = '_tail'
AUTH_OK = '_authOK'
AUTH_ERR = '_authERR'


def build(pars):
    res = bmcdata.bmc_data[ROOT]

    for p in pars.split(','):
        print p
        res += bmcdata.bmc_data[p]

    res += bmcdata.bmc_data[STATUS]
    res += bmcdata.bmc_data[TAIL]

    return res


def login(status):
    res = bmcdata.bmc_data[HEAD]
    res = bmcdata.bmc_data[ROOT]
    res += bmcdata.bmc_data[STATUS]
    res += bmcdata.bmc_data[AUTH_OK if status else AUTH_ERR]
    res += bmcdata.bmc_data[TAIL]

    return res


