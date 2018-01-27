#!/usr/bin/env python

import dbus
import dbus.service
import dbus.mainloop.glib
import LogBuffer
import LogMessage
import argparse
import gobject
import threading


class Service(dbus.service.Object):
    def __init__(self, message):
        super(Service, self).__init__()
        self._lock = threading.Lock()
        self._message = message
        self.parse_command_line_args()
        if self._args['depth'] is not None:
            self._log_buffer = LogBuffer.LogBuffer(self._args['depth'][0])
        else:
            self._log_buffer = LogBuffer.LogBuffer()

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName("com.project.logging.service", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/com/project/logging/service")
        self._loop = gobject.MainLoop()
        print "Service running..."
        self._loop.run()
        print "Service stopped"

    @dbus.service.method("com.project.logging.service.LogMessage", in_signature='sss', out_signature='b')
    def log_message(self, identity, level, message):
        try:
            self._lock.acquire()
            self._log_buffer.add_log_message(LogMessage.LogMessage(identity, level, message))
        finally:
            self._lock.release()
        return True

    @dbus.service.method("com.project.logging.service.Message", in_signature='', out_signature='s')
    def get_message(self):
        return self._message

    @dbus.service.method("com.project.logging.service.Clear", in_signature='', out_signature='')
    def clear(self):
        try:
            self._lock.acquire()
            print "Clearing Log"
            self._log_buffer.clear_buffer()
        finally:
            self._lock.release()

    @dbus.service.method("com.project.logging.service.Dump", in_signature='s', out_signature='s')
    def dump(self, level):
        try:
            self._lock.acquire()
            return self._log_buffer.dump_buffer(level)
        finally:
            self._lock.release()

    def parse_command_line_args(self):
        parser = argparse.ArgumentParser(description='Simple Logging service')
        parser.add_argument('-d', '--depth', type=int, nargs=1, help='Configure the log depth to store in memory default = 1000')
        self._args = vars(parser.parse_args())


if __name__ == "__main__":
    Service("Logging Service").run()
