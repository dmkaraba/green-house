#!/usr/bin/python
import time
import RPi.GPIO as GPIO
from config import gpio_pins_conf
import utils.logger as logger


class RelayBase(object):

    RELAY = None

    @classmethod
    def on(cls):
        GPIO.output(cls.RELAY, GPIO.LOW)
        return {'status': 'success', 'result': True}

    @classmethod
    def off(cls):
        GPIO.output(cls.RELAY, GPIO.HIGH)
        return {'status': 'success', 'result': False}

    @classmethod
    def switch(cls):
        switched_state = not GPIO.input(cls.RELAY)
        GPIO.output(cls.RELAY, switched_state)
        return {'status': 'success', 'result': not switched_state}

    @classmethod
    def get_state(cls):
        state = not GPIO.input(cls.RELAY)
        return {'status': 'success', 'result': state}

    @classmethod
    def set_up(cls):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(cls.RELAY, GPIO.OUT, initial=GPIO.HIGH)
        return {'status': 'success', 'info': 'GPIO {} set up'.format(cls.RELAY)}

    @classmethod
    def tear_down(cls):
        GPIO.cleanup()
        return {'status': 'success', 'info': 'GPIO {} cleaned up'.format(cls.RELAY)}


class Light(RelayBase):
    RELAY = gpio_pins_conf['relay_lights']


class Fan(RelayBase):
    RELAY = gpio_pins_conf['relay_fans']


class Pump(RelayBase):
    RELAY = [
        gpio_pins_conf['relay_pump_1'],
        # gpio_pins_conf['relay_pump_2']
    ]


class Servo(object):

    SERVO_PIN = gpio_pins_conf['servo']

    min_position = 3.0
    max_position = 12.4

    @staticmethod
    def get_state():
        pass

    @classmethod
    def set_state(cls, position=None, min=min_position, max=max_position):
        answer = dict()
        if position != None:
            if position <= 10 and position >= 0:
                new_pos = min+position*(max-min)/10
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(cls.SERVO_PIN, GPIO.OUT)
                pwm = GPIO.PWM(cls.SERVO_PIN, 50)
                pwm.start(5)
                pwm.ChangeDutyCycle(new_pos)
                time.sleep(1.5)
                pwm.stop()
                GPIO.cleanup()
                answer.update({'status': 'success', 'result': position})
                logger.info('Servo.set_state: new position is {}'.format(position))
            else:
                answer.update({'status': 'fail', 'info': 'Position out of range'})
                logger.warning('Servo.set_state: position {} not in [0:10]'.format(position))
        else:
            answer.update({'status': 'fail', 'info': 'No position provided'})
            logger.warning('Servo.set_state: no position provided')
        return answer
