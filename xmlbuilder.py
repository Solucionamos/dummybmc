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

HEAD = '<root>'
TAIL = '<status>ok</status></root>'

def build(pars):
    res = ''

    for p in pars.split(','):
        print p
        res += bmcdata.bmc_data[p]

    return HEAD + res + TAIL


