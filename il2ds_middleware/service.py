# -*- coding: utf-8 -*-

import datetime

from twisted.application.internet import TimerService
from twisted.application.service import Service
from twisted.internet import defer

from zope.interface import implementer

from il2ds_middleware.interface.service import IPilotService


class LogWatchingBaseService(TimerService):

    receiver = None

    def __init__(self, log_path, interval=1):
        self.log_file = None
        self.log_path = log_path
        TimerService.__init__(self, interval, self.do_watch)

    def do_watch(self):
        self.log_file.seek(self.log_file.tell())
        for line in self.log_file.readlines():
            self.got_line(line)

    def got_line(self, line):
        raise NotImplementedError

    def startService(self):
        if self.log_file is not None:
            return
        self.log_file = open(self.log_path, 'r')
        TimerService.startService(self)

    def stopService(self):
        if self.log_file is None:
            return defer.succeed(None)
        else:
            self.log_file.close()
            self.log_file = None
            return TimerService.stopService(self)


class LogWatchingService(LogWatchingBaseService):

    def got_line(self, line):
        if self.receiver is not None:
            timestamp = datetime.datetime.now()
            self.receiver.got_event_line(line, timestamp)


@implementer(IPilotService)
class PilotBaseService(Service):

    def __init__(self, console=None):
        self.console = console

    def user_join(self, info):
        raise NotImplementedError

    def user_left(self, info):
        raise NotImplementedError
