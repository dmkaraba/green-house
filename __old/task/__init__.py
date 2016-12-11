#!/usr/bin/python


class BaseMQTTDmn(object):

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = None
        self.pidfile_timeout = 5

    def run(self):
        raise NotImplementedError

# TODO: moved in modules_mqtt_interaction. Delete from here.