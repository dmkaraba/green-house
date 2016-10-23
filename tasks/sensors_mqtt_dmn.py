#!/usr/bin/python
import time
from daemon import runner
from tasks import BaseMQTTDmn
from utils.sensors.reader import read_all
from utils.cloud_mqtt_processor import GHMQTTClass
# from utils.cloud_mqtt_processor.sensors import pub_all


class SensorsMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(SensorsMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/sensors_mqtt_dmn.pid'

    def run(self):
        "Action that has to be continuosly rtun in a loop like daemon"
        while True:
            # pub_all()
            results = read_all()
            print results
            data = results['result']
            msgs = [
                ('conditions/luminosity', data['luminosity']),
                ('conditions/soil/temperature', data['soil_temperature']),
                ('conditions/air/outside/temperature', data['air_out_temperature']),
                ('conditions/air/inside/temperature', data['air_inside']['temperature']),
                ('conditions/air/inside/humidity', data['air_inside']['humidity'])
            ]
            GHMQTTClass().pub(msgs)
            time.sleep(10)


app = SensorsMQTTDmn()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()

# but in works
# SensorsMQTTDmn().run()