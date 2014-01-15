#!/usr/bin/env python
import Queue
import logging
import os
import requests
import sensor_threads
import argparse
import json

BUCKSTATS_TOKEN = os.environ['BUCKSTATS_TOKEN']

ONE_YEAR = 60 * 60 * 24 * 365

def save(message):
    event = {
        'event': message[0],
        'time': message[1],
    }
    requests.post(
        'http://localhost:5000/api/events',
        data=json.dumps(event),
        headers={
            'content-type': 'application/json',
            'token': BUCKSTATS_TOKEN,
        },
    )

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

    save(sensor_threads.msg('startup'))
    try:
        while True:
            # queue.get blocks Ctrl-C signal unless a timeout is
            # specified, even if the timeout will never be reached.
            message = queue.get(timeout=ONE_YEAR)
            logging.debug('Received message ' + str(message))
            save(message)
    finally:
        save(sensor_threads.msg('shutdown'))
