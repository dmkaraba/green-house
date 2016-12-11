#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal


class SensorsMQTTDmn(object):

    def __init__(self):
        self.kill_now = False

    def exit_pub_loop(self, signum, frame):
        # print 'exit_pub_loop'
        self.kill_now = True
        self.mqtt_connection.disconnect()

    def run(self):
        from utils.sensors.reader import read_all
        from modules.mqtt_interaction.base import Base_GHMQTT

        self.mqtt_connection = Base_GHMQTT()

        #TODO: missing ONE message while disconnect-reconnect
        while not self.kill_now:

            signal.signal(signal.SIGTERM, self.exit_pub_loop)
            signal.signal(signal.SIGINT, self.exit_pub_loop)

            results = read_all()
            if results:
                data = results['result']
                msgs = [
                    ('conditions/soil/temperature', data['soil']['temperature']),
                    ('conditions/soil/moisture', data['soil']['moisture']),
                    ('conditions/air/outside/temperature', data['air_outside']['temperature']),
                    ('conditions/air/inside/temperature', data['air_inside']['temperature']),
                    ('conditions/air/inside/humidity', data['air_inside']['humidity']),
                    ('conditions/air/inside/luminosity', data['air_inside']['luminosity']),
                ]
                self.mqtt_connection.pub(msgs)
            # print 'Steel in while loop'
            time.sleep(5)
