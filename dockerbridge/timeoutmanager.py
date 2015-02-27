"""
A generic timeout mechanism for multiple clients. Initialize with TimeoutManager(interval_in_seconds, callback).
When started, the manager will check every interval_in_seconds seconds, if any client ran into a timeout. If a client
ran into a timeout, the manager will call the callback function with the client name as argument. Start the manager with
start(), set the timeout for a client with setTimeout(client, seconds_from_now), or remove the timeout for a client with
remove(client). You can reset the timeout for a client by calling resetTimeout, this will refresh the timeout, if a
timeout was previously assigned to that client.
"""

from thread import start_new_thread
from time import sleep, time
from utils import sysout

__author__ = 'mhorst@cs.uni-bremen.de'


class TimeoutManager(object):
    def __init__(self, interval, callbackFunc):
        self.interval = interval
        self.callbackFunc = callbackFunc

    clients = dict()

    def start(self):
        return start_new_thread(self.__watchdog, ())

    def setTimeout(self, name, seconds):
        self.clients[name] = time() + seconds
        sysout('Timeout added for '+name+', terminating in '+str(seconds)+' seconds')

    def resetTimeout(self, name, seconds):
        if name in self.clients:
            self.clients[name] = time() + seconds
            sysout('Timeout reset for '+name+', terminating in '+str(seconds)+' seconds')

    def remove(self, name):
        if name in self.clients:
            del self.clients[name]

    def __watchdog(self):
        while True:
            currenttime = time()
            for name, timeleft in self.clients.copy().iteritems():
                if timeleft < currenttime:
                    self.callbackFunc(name)
                    self.remove(name)
                    sysout('Timeout reached for ' + name)
            sleep(self.interval)
