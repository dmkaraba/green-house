#!/usr/bin/python
from modules.greenhouse.sensors import DS18B20_Air, DS18B20_Soil
from modules.greenhouse.sensors import BH1750, DHT22, SoilMoistureSensors
from modules.greenhouse.controllers import Light, Fan, Pump, Servo
from time import sleep


def test_sensors():
    sensors = (DS18B20_Air, DS18B20_Soil, BH1750,
               DHT22, SoilMoistureSensors)
    for sensor in sensors:
        name, answer = sensor.NAME, sensor().read()
        if answer['status'] == 'success':
            value = answer['result']
            print 'OK   | {0:<33} | {1}'.format(name, value)
        else:
            print 'FAIL | {0:<33} | {1}'.format(name, answer['status'])

def test_relay_performers():

    performers = (Light, Fan, Pump)

    for perf in performers:
        print perf.on()
        sleep(1)
        print perf.off()
        sleep(1)

def test_servo():
    print Servo.set_state(0)
    sleep(1)
    print Servo.set_state(5)
    sleep(1)
    print Servo.set_state(10)
    sleep(1)
    print Servo.set_state(5)
    sleep(1)


if __name__ == '__main__':
    # test_relay_performers()
    # test_servo()
    test_sensors()
