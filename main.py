#!/usr/bin/env python
import sys

while True:
    line = sys.stdin.readline()
    if 'boolean true' in line:
        print 'screen locked'
    elif 'boolean false' in line:
        print 'screen unlocked'
