#!/usr/bin/env python3

import os
import pdb

ARCDIR = '/var/lib/sympa/arc'
ARCHIVES = os.listdir(ARCDIR)

for list in ARCHIVES:
    listdir = ARCDIR + '/list'
    breakpoint