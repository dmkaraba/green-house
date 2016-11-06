#!/usr/bin/python

from daemon.runner import DaemonRunner
from utils.cloud_mqtt_processor.performers import PumpsMQTTClass
from config import mqtt_topics_sub
from task import BaseMQTTDmn


class PumpsMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(PumpsMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/pumps_mqtt_dmn.pid'

    def run(self):
        PumpsMQTTClass().sub(mqtt_topics_sub['pumps'])


app = PumpsMQTTDmn()
daemon_runner = DaemonRunner(app)
daemon_runner.do_action()
