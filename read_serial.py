#!/usr/bin/env python
import serial

arduino = serial.Serial('/dev/ttyACM0', 9600)
for line in arduino:
    print line,
