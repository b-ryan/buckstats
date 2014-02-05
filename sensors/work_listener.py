#!/usr/bin/env python
import Queue
import logging
import os
import requests
import sensor_threads
import argparse
import json
import time

BUCKSTATS_TOKEN = os.environ['BUCKSTATS_TOKEN']

ONE_YEAR = 60 * 60 * 24 * 365

logging.basicConfig(level=logging.DEBUG)

def save(message, attempt=0):
    post_data = json.dumps({
        'event': message[0],
        'time': message[1],
    })
    logging.debug("sending event to API: " + post_data)
    try:
        response = requests.post(
            'https://data.buckryan.com/api/events',
            data=post_data,
            headers={
                'content-type': 'application/json',
                'token': BUCKSTATS_TOKEN,
            },
        )
    except Exception, e:
        logging.debug("Will retry after five seconds.")
        return save(message, attempt + 1)

    if response.status_code != requests.codes.created:
        logging.debug("API request failed with message: " + response.text)
        if attempt < 5:
            logging.debug("Will retry after five seconds.")
            time.sleep(5)
            return save(message, attempt + 1)
        else:
            logging.error("API request completely failed.")
            raise RuntimeError()

if __name__ == '__main__':
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
