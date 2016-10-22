#!/usr/bin/python
from daemon import runner
from utils.cloud_mqtt_processor.performers import LightsMQTTClass
from config import mqtt_topics_sub


class LightsMQTTDmn(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/lights_mqtt_dmn.pid'
        self.pidfile_timeout = 5
    def run(self):
        LightsMQTTClass().sub(mqtt_topics_sub['lights'])


app = LightsMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

