#!/usr/bin/python
import smbus
import time
import RPi.GPIO as GPIO
import Adafruit_DHT as dht
import Adafruit_ADS1x15
import utils.logger as logger
from config import gpio_pins_conf, sensor_ids


class BaseSensor(object):

    @classmethod
    def set_up(cls):
        raise NotImplementedError

    @classmethod
    def tear_down(cls):
        raise NotImplementedError

    @classmethod
    def read(cls):
        pass


class BH1750(BaseSensor):

    # Define some constants from the datasheet
    DEVICE = 0x23  # Default device I2C address

    POWER_DOWN = 0x00  # No active state
    POWER_ON = 0x01  # Power on
    RESET = 0x07  # Reset data register value

    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23

    # bus = smbus.SMBus(0) # Rev 1 Pi uses 0
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    def read(self):
        answer = dict()
        try:
            self.readLight()  # warming up
            time.sleep(0.5)
            luminosity = self.readLight()
            logger.info('BH1750| L: {}'.format(luminosity))
            answer.update({'status': 'success', 'result': float("%.1f" % luminosity)})
        except:
            logger.warning('BH1750 read fail')
            answer.update({'status': 'fail'})
        return answer

    def convertToNumber(self, data):
        # Simple function to convert 2 bytes of data
        # into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self, addr=DEVICE):
        data = self.bus.read_i2c_block_data(addr, self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)


class DHT22(BaseSensor):

    DHT22_PIN = gpio_pins_conf['DHT22']

    def read(self):
        answer = dict()
        try:
            h, t = dht.read_retry(dht.DHT22, self.DHT22_PIN, delay_seconds=3)
            h, t = float("%.1f" % h), float("%.1f" % t)
            logger.info('DHT22| T: {}, H: {}'.format(t, h))
            answer.update({"status": "success",
                           "result": {"temperature": t, "humidity": h}})
        except:
            logger.warning('DHT22 read fail')
            answer.update({"status": "fail"})
        return answer


class DS18B20(BaseSensor):

    SOIL = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_ids['ds18b20_a'])
    AIR = "/sys/bus/w1/devices/{}/w1_slave".format(sensor_ids['ds18b20_b'])

    def __init__(self, where_to_get='not_valid'):
        if where_to_get == 'air':
            self.sensor_file = self.AIR
        elif where_to_get == 'soil':
            self.sensor_file = self.SOIL
        else:
            self.sensor_file = 'not_valid'

    def read(self):
        answer = dict()
        if self.sensor_file != 'not_valid':
            temp = self.__read_temp(self.sensor_file)
            logger.info('DS18B20| T: {}'.format(temp))
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
            time.sleep(0.2)
            lines = self.__read_temp_raw(sensor_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1].strip()[equals_pos+2:]
            temp = float(temp_string) / 1000
            temp_formated = float("%.1f" % temp)
            return temp_formated


class SoilMoistureSensors(BaseSensor):

    GAIN = 1

    MIN_VOLTS = 0
    MAX_VOLTS = 25600

    adc = Adafruit_ADS1x15.ADS1115()

    def read_one_sensor(self, sens_num):
        """Read raw data from specific sensor [0...3]"""
        return self.adc.read_adc(sens_num, gain=self.GAIN)

    def read_all_sensors(self):
        """Read data from all sensors"""
        values = [0]*4
        for i in range(4):
            values[i] = self.adc.read_adc(i, gain=self.GAIN)
        return values

    def do_average(self, values):
        return sum(values)/len(values)

    def read(self):
        raw = self.read_all_sensors()
        percents = map(self.volts_to_percents, raw)
        result = self.do_average(percents)
        return {'status': 'success', 'result': result}

    def volts_to_percents(self, value):
        """
        Converting raw volts to moisture percents.
        """
        old_min = self.MAX_VOLTS
        old_max = self.MIN_VOLTS
        new_min = 0
        new_max = 100

        # Figure out how 'wide' each range is
        old_span = old_max - old_min
        new_span = new_max - new_min

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(value - old_min) / float(old_span)
        value_scaled_formated = float("%.3f" % value_scaled)

        return new_min + (value_scaled_formated * new_span)


if __name__ == '__main__':
    print SoilMoistureSensors().volts_to_percents(7700)