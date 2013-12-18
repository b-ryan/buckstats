#!/usr/bin/env python
import work_listener as w
import sys

delim = "\t" if len(sys.argv) == 1 else sys.argv[1]

def demo_set():
    w.save(('sitting', '2013-12-02 23:50:00',))
    w.save(('standing', '2013-12-02 23:50:30',))
    w.save(('locked', '2013-12-02 23:51:00',))
    w.save(('sitting', '2013-12-02 23:51:45',))
    w.save(('unlocked', '2013-12-02 23:52:10',))
    w.save(('standing', '2013-12-02 23:52:50',))
    w.save(('tracking_shutdown', '2013-12-02 23:52:50',))
    w.save(('standing', '2013-12-02 23:52:55',))
    w.save(('sitting', '2013-12-02 23:54:00',))
    w.save(('tracking_shutdown', '2013-12-02 23:55:00',))

connection = w.get_connection()
cursor = connection.cursor()
cursor.execute('SELECT event, time FROM events ORDER BY time ASC')

tracker = w.Tracker()

for event, time in cursor:
    tracker.receive_event(event, time)

for i, line in enumerate(tracker.times):
    print delim.join(map(str, [i] + line))
