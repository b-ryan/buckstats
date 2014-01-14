#!/usr/bin/env python
import Queue
import logging
import psycopg2
import os
import requests
import sensor_threads
import argparse

BUCKSTATS_TOKEN = os.environ['BUCKSTATS_TOKEN']

ONE_YEAR = 60 * 60 * 24 * 365

class Tracker:

    def __init__(self):
        self.times = []
        self.position = 'sitting'
        self.lock_status = 'tracking_shutdown'

    def receive_event(self, event, time):
        last_row = self.times[-1] if len(self.times) else None

        if last_row and not last_row[2]:
            ## there is a sitting/standing event waiting to be closed
            # no matter what the event, we need to close that one out
            last_row[2] = time
            self.times[-1] = last_row

        if event in ('sitting', 'standing',):
            if self.lock_status != 'locked':
                self.times.append([event, time, None])
            self.position = event

        elif event == 'unlocked':
            assert(last_row)
            self.times.append([self.position, time, None])
            self.lock_status = event

        elif event in ('locked', 'tracking_shutdown',):
            self.lock_status = event

def get_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='stand',
        user='stand',
        password='password',
    )

def save(event):
    logging.debug(event)
    return
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT into events (event, time)
        VALUES (%s, %s)
        ''',
        event
    )
    connection.commit()
    connection.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--sensors', default='arduino,screen')
    args = parser.parse_args()

    queue = Queue.Queue()
    sensors = args.sensors.split(',')

    if 'arduino' in sensors:
        sensor_threads.ArduinoThread(queue).start()

    if 'screen' in sensors:
        sensor_threads.LockThread(queue).start()

    if 'stdin' in sensors:
        sensor_threads.StdinThread(queue).start()

    logging.info('Reading from queue')

    try:
        while True:
            # queue.get blocks Ctrl-C signal unless a timeout is
            # specified, even if the timeout will never be reached.
            message = queue.get(timeout=ONE_YEAR)
            logging.debug('Received message ' + str(message))
            save(message)
    finally:
        save(sensor_threads.msg('tracking_shutdown'))
