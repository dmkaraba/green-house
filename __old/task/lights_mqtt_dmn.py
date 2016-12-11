#!/usr/bin/python
from daemon.runner import DaemonRunner
from task import BaseMQTTDmn
from utils.cloud_mqtt_processor.performers import LightMQTTClass

# from config import mqtt_topics_sub


class LightMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(LightMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/lights_mqtt_dmn.pid'

    def run(self):
        LightMQTTClass().sub(mqtt_topics_sub['lights'])


app = LightMQTTDmn()
daemon_runner = DaemonRunner(app)
daemon_runner.do_action()