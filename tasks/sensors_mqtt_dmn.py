#!/usr/bin/python
import time
import signal
from daemon.runner import DaemonRunner
from tasks import BaseMQTTDmn


class SensorsMQTTDmn(BaseMQTTDmn):

    def __init__(self):
        super(SensorsMQTTDmn, self).__init__()
        self.pidfile_path = '/tmp/sensors_mqtt_dmn.pid'
        self.kill_now = False

    def exit_pub_loop(self, signum, frame):
        # print 'exit_pub_loop'
        self.kill_now = True

    def run(self):
        from utils.sensors.reader import read_all
        from utils.cloud_mqtt_processor import Base_GHMQTT

        mqtt_connection = Base_GHMQTT()

        while not self.kill_now:

            signal.signal(signal.SIGTERM, self.exit_pub_loop)
            signal.signal(signal.SIGINT, self.exit_pub_loop)

            results = read_all()
            data = results['result']
            msgs = [
                ('conditions/luminosity', data['luminosity']),
                ('conditions/soil/temperature', data['soil_temperature']),
                ('conditions/air/outside/temperature', data['air_out_temperature']),
                ('conditions/air/inside/temperature', data['air_inside']['temperature']),
                ('conditions/air/inside/humidity', data['air_inside']['humidity'])
            ]
            # print 'Steel in while loop'
            mqtt_connection.pub(msgs)
            time.sleep(5)


app = SensorsMQTTDmn()
daemon_runner = DaemonRunner(app)
daemon_runner.daemon_context.working_directory = '/home/pi/dev/green-house'
daemon_runner.do_action()
