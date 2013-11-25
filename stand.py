#!/usr/bin/env python
import time
import serial
import threading
import Queue
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import logging
import psycopg2

ONE_YEAR = 60 * 60 * 24 * 365

def dt():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def msg(event):
    return (event, dt(),)

class _Worker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def send_event(self, event):
        message = msg(event)
        logging.debug('Queuing ' + str(message))
        self.queue.put(message)

class ArduinoThread(_Worker):

    def run(self):
        logging.info('Starting arduino thread')
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        while True:
            line = arduino.readline().replace("\r\n", "\n")
            sitting_standing = line[:-1]
            assert(sitting_standing in ('sitting', 'standing',))
            self.send_event(sitting_standing)

class LockThread(_Worker):

    def run(self):
        logging.info('Starting lock thread')
        def cbk(message):
            unlocked = 0
            locked = 1
            assert(message in (unlocked, locked,))
            self.send_event(
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
        gobject.threads_init()
        loop.run()

def save(message):
    connection = psycopg2.connect(
        host='127.0.0.1',
        database='stand',
        user='stand',
        password='password',
    )
    cursor = connection.cursor()
    cursor.execute('''
        INSERT into events (event, time)
        VALUES (%s, %s)
        ''',
        message
    )
    connection.commit()
    connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    queue = Queue.Queue()
    ArduinoThread(queue).start()
    LockThread(queue).start()

    logging.info('Reading from queue')

    try:
        while True:
            # queue.get blocks Ctrl-C signal unless a timeout is
            # specified, even if the timeout will never be reached.
            message = queue.get(timeout=ONE_YEAR)
            logging.debug('Received message ' + str(message))
            save(message)
    finally:
        save(msg('tracking_shutdown'))
