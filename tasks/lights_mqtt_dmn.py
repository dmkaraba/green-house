#!/usr/bin/python
from daemon import runner
from utils.cloud_mqtt_processor.performers import LightsMQTTClass
from config import mqtt_topics_sub
from tasks import BaseMQTTDmn


class LightsMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(LightsMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/lights_mqtt_dmn.pid'

    def run(self):
        "Action that has to be continuosly rtun in a loop like daemon"
        LightsMQTTClass().sub(mqtt_topics_sub['lights'])


app = LightsMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

