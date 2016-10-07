#!/usr/bin/python
import time
import utils.logger as logger
from config import sensor_ids
from measurements import BaseSensor


class DS18B20(BaseSensor):

    SOIL = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_ids['ds18b20_a'])
    AIR = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_ids['ds18b20_b'])

    def __init__(self, what_to_get='not_valid'):
        if what_to_get == 'air':
            self.sensor_file = self.AIR
        elif what_to_get == 'soil':
            self.sensor_file = self.SOIL
        else:
            self.sensor_file = 'not_valid'

    def do_measure(self):
        answer = dict()
        if self.sensor_file != 'not_valid':
            temp = self.__read_temp(self.sensor_file)
            logger.info('DS18B20 askes. T: {}'.format(temp))
            answer.update({'status': 'success', 'result': temp})
        else:
            logger.warning('DS18B20 not valid file')
            answer.update({'status': 'fail', 'details': 'Not valid file address'})
        return answer

    def __read_temp_raw(self, sensor_file):
        with open(sensor_file, 'r') as f:
            lines = f.readlines()
        return lines

    def __read_temp(self, sensor_file):
        lines = self.__read_temp_raw(sensor_file)
        while lines[0].strip()[-3:] != 'YES':
            print 1
            time.sleep(0.2)
            lines = self.__read_temp_raw(sensor_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1].strip()[equals_pos+2:]
            temp = float(temp_string) / 1000
            return temp
