#!/usr/bin/python
from handlers.sensors import DS18B20, BH1750, DHT22
from handlers.controllers import Light, Fan, Pump, Servo
from time import sleep


def test_sensors():
    print 'Air temp outside: ' + str(DS18B20('air').read())
    print 'Air inside: ' + str(DHT22().read())
    print 'Soil temp: ' + str(DS18B20('soil').read())
    print 'Luminosity: ' + str(BH1750().read())

def test_relay_performers():

    performers = [Light, Fan]  #, Pump]

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
    test_relay_performers()
    test_servo()
    test_sensors()
