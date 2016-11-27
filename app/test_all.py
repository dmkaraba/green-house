#!/usr/bin/python
from handlers.sensors import DS18B20_Air, DS18B20_Soil
from handlers.sensors import BH1750, DHT22, SoilMoistureSensors
from handlers.controllers import Light, Fan, Pump, Servo
from time import sleep


def test_sensors():
    sensors = (DS18B20_Air, DS18B20_Soil, BH1750,
               DHT22, SoilMoistureSensors)
    for sensor in sensors:
        name, result = sensor.NAME, sensor().read()
        status, value = result['status'], result['result']
        if status == 'success':
            print 'OK | {0:<33} | {1}'.format(name, value)
        else:
            print 'FAIL | status: {}'.format(status)

def test_relay_performers():

    performers = (Light, Fan)  #, Pump)

    for perf in performers:
        print perf.set_up()
        print perf.on()
        sleep(2)
        print perf.off()
        print perf.tear_down()
        sleep(0.5)

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
