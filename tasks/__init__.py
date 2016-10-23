#!/usr/bin/python


class BaseMQTTDmn(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = None
        self.pidfile_timeout = 5
    def run(self):
        raise NotImplementedError
