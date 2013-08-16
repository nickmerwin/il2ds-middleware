# -*- coding: utf-8 -*-

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
from twisted.python import log


class ConsoleProtocol(LineOnlyReceiver):

    def lineReceived(self, line):
        if line == '' or line == "exit\\n":
            log.err("Game server is shut down")
            reactor.stop()
            return
        if line.startswith("<consoleN>"):
            return
        if line.endswith("\\n"):
            line = line[:-2]
        if line.startswith("\\u0020"):
            line = " " + line[6:]
        # TODO:


class ConsoleClientFactory(ClientFactory):
    protocol = ConsoleProtocol

    def clientConnectionFailed(self, connector, reason):
        log.err("Connection failed: %s" % reason)
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        log.err("Connection lost: %s" % reason)
        reactor.stop()