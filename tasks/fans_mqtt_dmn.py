#!/usr/bin/python
from daemon import runner
from utils.cloud_mqtt_processor.performers import FansMQTTClass
from config import mqtt_topics_sub
from tasks import BaseMQTTDmn


class FansMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(FansMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/fans_mqtt_dmn.pid'

    def run(self):
        "Action that has to be continuosly rtun in a loop like daemon"
        FansMQTTClass().sub(mqtt_topics_sub['fans'])


app = FansMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
