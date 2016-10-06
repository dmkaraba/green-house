

class Base(object):

    print 'body'

    @classmethod
    def on(cls):
        print 'on'

    def __call__(self, *args, **kwargs):
        print 'call'

    def __new__(cls, *args, **kwargs):
        print 'new'



import time
import utils.logger as logger
from config import sensor_ids
from measurements import BaseSensor


class DS18B20(BaseSensor):

    sensor_a_id = sensor_ids['ds18b20_a']
    sensor_b_id = sensor_ids['ds18b20_b']
    sensor_a_file = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_a_id)
    sensor_b_file = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_b_id)

    @classmethod
    def do_measure(cls):
        pass

    def red_temp_raw(self, sensor_file):
        with open(sensor_file, 'r') as f:
            lines = f.readline()
        return lines

    def read_temp(self):
        pass