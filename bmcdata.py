#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

from collections import defaultdict

data = {'pwState':'<pwState>1</pwState>',
        'customerSpecificPowerSupplies': '',
        'customerSpecificPowerUnit': '',
        'snmpCommunity': '',
        'snmpTrapDest2Ena': '',
        'getPEF': '',
        'fans': '',
        'voltages': '',
        'temperatures': '',
}

bmc_data = defaultdict(str)

for k in data:
    bmc_data[k] = data[k]

