#!/usr/bin/python
import paho.mqtt.client as mqtt
import json
import time
import signal
from config import cloud_mqtt_cred


class GHMQTTClass(mqtt.Client):

    USERNAME = cloud_mqtt_cred['user']
    PASSWORD = cloud_mqtt_cred['pass']
    SERVER = cloud_mqtt_cred['server']

    def __init__(self):
        super(GHMQTTClass, self).__init__()
        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self, signum, frame):
        print signum, frame
        self.disconnect()

    def on_connect(self, mqttc, obj, flags, rc):
        print("Connected rc: "+str(rc))

    def on_disconnect(self, mqttc, userdata, rc):
        print("Dissconnected rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        print("Message"+msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("Published mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def perform(self, mqttc, obj, msg):
        raise NotImplementedError

    def pub(self, msgs):
        self.username_pw_set(self.USERNAME, self.PASSWORD)
        self.connect(self.SERVER, 10990, 60)
        for topic, payload in msgs:
            self.publish(topic, json.dumps(payload))

    def sub(self, topic):
        # self.on_message = self.on_message
        self.username_pw_set(self.USERNAME, self.PASSWORD)
        self.connect(self.SERVER, 10990, 60)
        self.subscribe(topic, 0)
        # self.loop_forever()

        # self.loop_start()
        rc = 0
        while rc == 0:
            rc = self.loop()
        # self.loop_stop()
        # self.disconnect()

        # rc = 0
        # while rc == 0:
        #     rc = self.loop()
        # return rc

# def cleanup():

# Use the signal module to handle signals
