#!/usr/bin/env python
import stand

def demo_set():
    stand.save(('sitting', '2013-12-02 23:50:00',))
    stand.save(('standing', '2013-12-02 23:50:30',))
    stand.save(('locked', '2013-12-02 23:51:00',))
    stand.save(('sitting', '2013-12-02 23:51:45',))
    stand.save(('locked', '2013-12-02 23:52:00',))
    stand.save(('unlocked', '2013-12-02 23:52:10',))
    stand.save(('standing', '2013-12-02 23:52:50',))
    stand.save(('tracking_shutdown', '2013-12-02 23:52:50',))
    stand.save(('standing', '2013-12-02 23:52:55',))
    stand.save(('sitting', '2013-12-02 23:54:00',))
    stand.save(('tracking_shutdown', '2013-12-02 23:55:00',))

connection = stand.get_connection()
cursor = connection.cursor()
cursor.execute('SELECT event, time FROM events ORDER BY time ASC')

status = None
start_time = None

for event, time in cursor:
    if event in ('sitting', 'standing',) and event != status:
        if start_time:
            print status, 'for', time - start_time
        status = event
        start_time = time
    elif event in ('locked', 'tracking_shutdown',):
        if start_time:
            print status, 'for', time - start_time
        start_time = None
    elif event in ('unlocked',):
        start_time = time
