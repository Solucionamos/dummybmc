#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

import os
from collections import defaultdict

XML_DIR = 'xmldata'
bmc_data = defaultdict(str)

for filename in os.listdir(XML_DIR):
    name, _ = filename.split('.')
    bmc_data[name] = file(os.path.join(XML_DIR, filename), 'r').read()

# print bmc_data

