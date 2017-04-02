#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
import utils.logger as logger
from config import config


class RelayBase(object):
    """
    Controlling relay performers here.
    Usage (lights for example):

    # If we want to switch lights on
    Light.on()

    # If we want to switch lights off
    Light.off()

    # We cat reverse lights state
    Light.switch()

    # We can ask for lights state
    Light.get_state()

    # We can set up lights  GPIO  pins  before turning on.
    # But it's not necessary. Just turning on or switching
    # checks for GPIOs for been seted up.
    # And if they are not yet it sets them up.
    """

    RELAY = None
    SETED_UP = False

    @classmethod
    def on(cls):
        if not cls.SETED_UP:
            cls.set_up()
        GPIO.output(cls.RELAY, GPIO.LOW)
        return {'status': 'success', 'result': True}

    @classmethod
    def off(cls):
        if cls.SETED_UP:
            GPIO.output(cls.RELAY, GPIO.HIGH)
            return {'status': 'success', 'result': False, 'msg': 'turned off'}  # TODO: rebuild to answer objects
        else:
            return {'status': 'success', 'result': False, 'msg': 'was not seted up'}

    @classmethod
    def switch(cls):
        if not cls.SETED_UP:
            cls.set_up()
        switched_state = not GPIO.input(cls.RELAY)
        GPIO.output(cls.RELAY, switched_state)
        return {'status': 'success', 'result': not switched_state}

    @classmethod
    def get_state(cls):
        if cls.SETED_UP:
            # We get the state of relay here. <not> is used
            # because of getting human readable result:
            # GPIO.LOW -> relay is locked (ON) -> True
            # GPIO.HIGH -> relay is unlocked (OFF) -> False
            state = not GPIO.input(cls.RELAY)
            return {'status': 'success', 'result': state}
        else:
            return {'status': 'success', 'result': False}

    @classmethod
    def set_up(cls):
        if not cls.SETED_UP:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(cls.RELAY, GPIO.OUT, initial=GPIO.HIGH)
            cls.SETED_UP = True
            return {'status': 'success',
                    'info': 'GPIO {} seted up'.format(cls.RELAY)}
        else:
            return {'status': 'success',
                    'info': 'GPIO {} is already seted up'.format(cls.RELAY)}

    @classmethod
    def tear_down(cls):
        # TODO: not to call cleanup at all. Only at system shotdown
        GPIO.cleanup(cls.RELAY)
        cls.SETED_UP = False
        return {'status': 'success', 'info': 'GPIOs cleaned up'}


class Light(RelayBase):
    RELAY = config.relays['gpio_pins']['lights']


class Fan(RelayBase):
    RELAY = config.relays['gpio_pins']['fans']


class Pump(RelayBase):
    RELAY = [
        config.relays['gpio_pins']['pump_1'],
        config.relays['gpio_pins']['pump_2']
    ]

    @classmethod
    def pulse(cls, duration=1):
        cls.on()
        time.sleep(duration)
        cls.off()
        cls.tear_down()


class Servo(object):

    SERVO_PIN = config.relays['gpio_pins']['servo']

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
