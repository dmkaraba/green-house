#!/usr/bin/python

import RPi.GPIO as GPIO


def cleanup():
    GPIO.cleanup()