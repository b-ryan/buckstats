#!/usr/bin/env python
import time

def screen_saver_message_received(message):
    AWAY_FROM_COMPUTER = 1
    AT_COMPUTER = 0

    print time.strftime('%Y-%m-%d %H:%M:%S'),
    if message == AWAY_FROM_COMPUTER:
        print "I'm away from my computer"
    elif message == AT_COMPUTER:
        print "I'm at my computer"
    else:
        print "Wft, mate?", message, type(message)

import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_signal_receiver(
    screen_saver_message_received,
    dbus_interface='org.gnome.ScreenSaver',
    signal_name='ActiveChanged'
)

loop = gobject.MainLoop()
loop.run()
