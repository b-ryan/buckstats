#!/bin/bash
dbus-monitor --session "type='signal',interface='org.gnome.ScreenSaver',member='ActiveChanged'" | ./main.py
