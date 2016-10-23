from handlers.controllers import Lights
from utils.cloud_mqtt_processor import GHMQTTClass
from config import mqtt_topics_pub
import json


class LightsMQTTClass(GHMQTTClass):

    topic_pub = mqtt_topics_pub['lights']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            Lights.set_up()
            Lights.on()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            Lights.off()
            Lights.tear_down()
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class FansMQTTClass(GHMQTTClass):

    topic_pub = mqtt_topics_pub['fans']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))


class PumpsMQTTClass(GHMQTTClass):

    topic_pub = mqtt_topics_pub['pumps']

    def on_message(self, mqttc, obj, msg):
        if msg.payload == 'on':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        elif msg.payload == 'off':
            self.publish(self.topic_pub, json.dumps({'status': 'ok'}))
        else:
            self.publish(self.topic_pub, json.dumps({'status': 'error'}))
