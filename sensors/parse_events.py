#!/usr/bin/env python
import sys

delim = "\t" if len(sys.argv) == 1 else sys.argv[1]

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

connection = get_connection()
cursor = connection.cursor()
cursor.execute('SELECT event, time FROM events ORDER BY time ASC')

tracker = Tracker()

for event, time in cursor:
    tracker.receive_event(event, time)

print delim.join(('id', 'position', 'start_time', 'end_time',))
for i, line in enumerate(tracker.times):
    print delim.join(map(lambda x: str(x) if x is not None else '', [i] + line))
