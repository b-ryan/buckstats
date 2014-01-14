import threading
import serial
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

class ListenerThread(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue

    def send_event(self, event):
        message = msg(event)
        logging.debug('Queuing ' + str(message))
        self.queue.put(message)

class ArduinoThread(ListenerThread):

    def run(self):
        logging.info('Starting arduino thread')
        arduino = serial.Serial('/dev/ttyACM0', 9600)
        while True:
            line = arduino.readline().replace("\r\n", "\n")[:-1]
            pre = "event: " 
            if pre in line:
                start = line.find(pre) + len(pre)
                sitting_standing = line[start:]
                assert(sitting_standing in ('sitting', 'standing',))
                self.send_event(sitting_standing)

class LockThread(ListenerThread):

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
