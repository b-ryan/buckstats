#!/usr/bin/env python
import time
import serial
import threading
import Queue
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import logging

def timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S')

class _Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def send_message(self, message):
        self.queue.put(message)

class ArduinoThread(_Worker):

    def run(self):
        logging.info('Starting arduino thread')
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        while True:
            line = arduino.readline()[:-1]
            self.send_message(line)

class LockThread(_Worker):

    def run(self):
        logging.info('Starting lock thread')
        def cbk(message):
            unlocked = 0
            locked = 1
            assert(message in (unlocked, locked,))
            self.send_message(
                'locked' if message == locked else 'unlocked'
            )

        DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        bus.add_signal_receiver(
            cbk,
            dbus_interface='org.gnome.ScreenSaver',
            signal_name='ActiveChanged'
        )
        loop = gobject.MainLoop()
        loop.run()

logging.basicConfig(level=logging.INFO)
queue = Queue.Queue()
ArduinoThread(queue).start()
# LockThread(queue).start()

logging.info('Reading from queue')
while True:
    try:
        # queue.get blocks Ctrl-C signal unless a timeout is specified,
        # even if the timeout will never be reached.
        ONE_YEAR = 60 * 60 * 24 * 365
        message = queue.get(timeout=ONE_YEAR)
    except Queue.Empty:
        pass
    else:
        logging.info('Message received: ' + message)
