#!/usr/bin/python
from daemon import runner
from utils.cloud_mqtt_processor.performers import PumpsMQTTClass
from config import mqtt_topics_sub


class PumpsMQTTDmn(object):
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/tmp/pumps_mqtt_dmn.pid'
        self.pidfile_timeout = 5
    def run(self):
        PumpsMQTTClass().sub(mqtt_topics_sub['pumps'])


app = PumpsMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()


