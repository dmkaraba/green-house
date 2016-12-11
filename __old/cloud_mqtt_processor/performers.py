#!/usr/bin/python
import json

from utils.cloud_mqtt_processor import Base_GHMQTT

# from config import config
from handlers.controllers import Light, Fan, Pump


class LightMQTTClass(Base_GHMQTT):

    topic_pub = config['mqtt_topics_pub']['lights']

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

    topic_pub = config['mqtt_topics_pub']['fans']

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

    topic_pub = config['mqtt_topics_pub']['pumps']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Pump.pulse(5)
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Pump.off()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))
