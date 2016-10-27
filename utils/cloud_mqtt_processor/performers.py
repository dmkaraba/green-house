#!/usr/bin/python
from handlers.controllers import Light, Fan, Pump
from utils.cloud_mqtt_processor import Base_GHMQTT
from config import mqtt_topics_pub
import json


class LightMQTTClass(Base_GHMQTT):

    topic_pub = mqtt_topics_pub['lights']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Light.set_up()
            Light.on()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Light.off()
            Light.tear_down()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class FansMQTTClass(Base_GHMQTT):

    topic_pub = mqtt_topics_pub['fans']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class PumpsMQTTClass(Base_GHMQTT):

    topic_pub = mqtt_topics_pub['pumps']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))
