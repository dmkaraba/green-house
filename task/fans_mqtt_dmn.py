#!/usr/bin/python
from daemon.runner import DaemonRunner
from utils.cloud_mqtt_processor.performers import FansMQTTClass
from config import mqtt_topics_sub
from task import BaseMQTTDmn


class FansMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(FansMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/fans_mqtt_dmn.pid'

    def run(self):
        FansMQTTClass().sub(mqtt_topics_sub['fans'])


app = FansMQTTDmn()
daemon_runner = DaemonRunner(app)
daemon_runner.do_action()
