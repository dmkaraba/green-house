#!/usr/bin/python

import time
import Adafruit_ADS1x15
import Adafruit_DHT as dht
import smbus
import utils.logger as logger
from config import config
from modules.greenhouse.sensor_answers import DS18B20Result, BH1750Result, DHT22Result, SoilMoistureResult


class BaseSensor(object):

    NAME = None

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

    NAME = 'Air inside luminosity'

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
        try:
            self.readLight()  # warming up
            time.sleep(0.5)
            luminosity = self.readLight()
            logger.info('BH1750| L: {}'.format(luminosity))
            return BH1750Result({'luminosity': float("%.1f" % luminosity)})
        except IOError:
            return BH1750Result({'rc': 66})

    def convertToNumber(self, data):
        # Simple function to convert 2 bytes of data
        # into a decimal number
        return ((data[1] + (256 * data[0])) / 1.2)

    def readLight(self, addr=DEVICE):
        data = self.bus.read_i2c_block_data(addr, self.ONE_TIME_HIGH_RES_MODE_1)
        return self.convertToNumber(data)


class DHT22(BaseSensor):

    NAME = 'Air inside humidity/temperature'
    DHT22_PIN = config.sensors['gpio_pins']['DHT22']

    def read(self):
        h, t = dht.read_retry(dht.DHT22, self.DHT22_PIN, delay_seconds=3)
        logger.info('DHT22| T: {}, H: {}'.format(t, h))
        DHT22Result.temperature = float("%.1f" % t)
        DHT22Result.humidity = float("%.1f" % h)
        return DHT22Result({'temperature': float("%.1f" % t), 'humidity': float("%.1f" % h)})


class DS18B20(BaseSensor):

    NAME = None
    SENSOR_FILE = None

    def read(self):
        t = self.__read_temp(self.SENSOR_FILE)
        logger.info('DS18B20| T: {}'.format(t))
        return DS18B20Result({'temperature': t})

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


class DS18B20_Air(DS18B20):
    NAME = 'Air outside temperature'
    SENSOR_FILE = "/sys/bus/w1/devices/{}/w1_slave".format(config.sensors['ids']['ds18b20_b'])


class DS18B20_Soil(DS18B20):
    NAME = 'Soil inside temperature'
    SENSOR_FILE = "/sys/bus/w1/devices/{}/w1_slave".format(config.sensors['ids']['ds18b20_a'])


class SoilMoistureSensors(BaseSensor):

    NAME = 'Soil moisture'
    GAIN = 1
    MIN_VOLTS = 4700
    MAX_VOLTS = 18000

    adc = Adafruit_ADS1x15.ADS1115()

    def read_one_raw(self, sens_num):
        """Read raw data from specific sensor [0...3]"""
        return self.adc.read_adc(sens_num, gain=self.GAIN)

    def read_all_raw(self):
        """Read data from all sensors"""
        values = [0]*4
        for i in range(4):
            values[i] = self.adc.read_adc(i, gain=self.GAIN)
        return values

    def do_average(self, values):
        return sum(values)/len(values)

    def volts_to_percents(self, value):
        """
        Converting raw volts to moisture percents.
        """
        old_min = self.MIN_VOLTS
        old_max = self.MAX_VOLTS
        new_min = 0
        new_max = 100

        # Figure out how 'wide' each range is
        old_span = old_max - old_min
        new_span = new_max - new_min

        # Convert the left range into a 0-1 range (float)
        value_scaled = float(value - old_min) / float(old_span)
        value_scaled_formated = float("%.3f" % value_scaled)

        return new_min + (value_scaled_formated * new_span)

    def read(self):
        raw = self.read_all_raw()
        percents = map(self.volts_to_percents, raw)
        return SoilMoistureResult({'moisture': self.do_average(percents)})

    def read_one(self, num):
        raw = self.read_one_raw(num)
        result = map(self.volts_to_percents, [raw])[0]
        return SoilMoistureResult({'moisture': result})


class SoilMoistureA(SoilMoistureSensors):
    def read(self):
        result1 = self.read_one(0)
        result2 = self.read_one(1)
        avg = (result1.moisture + result2.moisture)/2
        return SoilMoistureResult({'moisture': avg})


class SoilMoistureB(SoilMoistureSensors):
    def read(self):
        result1 = self.read_one(2)
        result2 = self.read_one(3)
        avg = (result1.moisture + result2.moisture)/2
        return SoilMoistureResult({'moisture': avg})
