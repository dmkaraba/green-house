#!/usr/bin/python
from daemon import runner
from utils.cloud_mqtt_processor.performers import FansMQTTClass
from config import mqtt_topics_sub


class FansMQTTDmn(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/fans_mqtt_dmn.pid'
        self.pidfile_timeout = 5
    def run(self):
        FansMQTTClass().sub(mqtt_topics_sub['fans'])


app = FansMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()


