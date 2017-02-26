#!/usr/bin/python

import RPi.GPIO as GPIO


def cleanup():
    GPIO.cleanup()


if __name__ == '__main__':
    cleanup()
