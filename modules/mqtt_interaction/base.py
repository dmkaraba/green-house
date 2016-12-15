#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import signal

import paho.mqtt.client as mqtt

from config import config
from modules.greenhouse.controllers import Light, Fan, Pump


class Base_GHMQTT(mqtt.Client):

    USERNAME = config.cloud_mqtt_cred['user']
    PASSWORD = config.cloud_mqtt_cred['pass']
    SERVER = config.cloud_mqtt_cred['server']

    def __init__(self):
        super(Base_GHMQTT, self).__init__()

        self.username_pw_set(self.USERNAME, self.PASSWORD)
        self.connect(self.SERVER, 10990, 60)

        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self, signum, frame):
        # print signum, frame
        self.disconnect()
        print '>>> Base_GHMQTT:cleanup'

    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected rc: "+str(rc))

    def on_disconnect(self, mqttc, userdata, rc):
        print("Dissconnected rc: " + str(rc))
        if rc != 0:
            self.reconnect()
            print "Reconnected"

    def on_message(self, mqttc, obj, msg):
        print("Message "+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("Published mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def perform(self, mqttc, obj, msg):
        raise NotImplementedError

    def pub(self, msgs):
        for topic, payload in msgs:
            self.publish(topic, json.dumps(payload))

    def sub(self, topic):
        print '>>>sub(topic={})'.format(topic)
        self.subscribe(topic, 0)

        rc = 0
        while rc == 0:
            rc = self.loop()

        return rc


class LightMQTTClass(Base_GHMQTT):

    topic_pub = config.mqtt_topics_pub['lights']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Light.on()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Light.off()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class FansMQTTClass(Base_GHMQTT):

    topic_pub = config.mqtt_topics_pub['fans']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Fan.on()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Fan.off()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class PumpsMQTTClass(Base_GHMQTT):

    topic_pub = config.mqtt_topics_pub['pumps']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Pump.pulse(5)
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Pump.off()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))
