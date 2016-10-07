#!/usr/bin/python
import time
import RPi.GPIO as GPIO
import utils.logger as logger
from config import gpio_pins_conf


SERVO_PIN = gpio_pins_conf['servo']


class Servo(object):

    min_position = 3.0
    max_position = 12.4

    @staticmethod
    def get_state():
        pass

    @staticmethod
    def set_state(position=None, min=min_position, max=max_position):
        answer = dict()
        if position != None:
            if position <= 10 and position >= 0:
                new_pos = min+position*(max-min)/10
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(SERVO_PIN, GPIO.OUT)
                pwm = GPIO.PWM(SERVO_PIN, 50)
                pwm.start(5)
                pwm.ChangeDutyCycle(new_pos)
                time.sleep(1.5)
                pwm.stop()
                GPIO.cleanup()
                answer.update({'status': 'success', 'result': position})
                logger.info('Servo.set_state: new position is {}'.format(position))
            else:
                answer.update({'status': 'fail'})
                logger.warning('Servo.set_state: position {} not in [0:10]'.format(position))
        else:
            answer.update({'status': 'fail'})
            logger.warning('Servo.set_state: no argument passed')
        return answer


if __name__=='__main__':
    print Servo.set_state(0)
    time.sleep(1)
    print Servo.set_state(5)
    time.sleep(1)
    print Servo.set_state(10)
    time.sleep(1)
    print Servo.set_state(5)
