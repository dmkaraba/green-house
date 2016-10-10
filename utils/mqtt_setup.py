#!/usr/bin/python
import paho.mqtt.client as mqtt
import json


# def on_connect(mqttc, obj, flags, rc):
#     print("rc: "+str(rc))
#
#
# def on_publish(mqttc, obj, mid):
#     print("mid: "+str(mid))
#
#
# def on_subscribe(mqttc, obj, mid, granted_qos):
#     print("Subscribed: "+str(mid)+" "+str(granted_qos))
#
#
# def on_message(mqttc, obj, msg):
#     print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
#
#
# def publish(msgs):
#     mqttc = mqtt.Client()
#     mqttc.on_connect = on_connect
#     mqttc.on_publish = on_publish
#     mqttc.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
#     mqttc.connect("m21.cloudmqtt.com", 10990, 60)
#     for topic, payload in msgs:
#         mqttc.publish(topic, json.dumps(payload))
#     mqttc.disconnect()
#
#
# def subscribe():
#     mqttc = mqtt.Client()
#     mqttc.on_message = on_message
#     mqttc.on_connect = on_connect
#     mqttc.on_publish = on_publish
#     mqttc.on_subscribe = on_subscribe
#     mqttc.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
#     mqttc.connect("m21.cloudmqtt.com", 10990, 60)
#     mqttc.subscribe("greenhouse/#", 0)
#     mqttc.loop_forever()



class GHMQTTClass(mqtt.Client):

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def pub(self, msgs):
        self.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
        self.connect("m21.cloudmqtt.com", 10990, 60)
        for topic, payload in msgs:
            self.publish(topic, json.dumps(payload))

    def sub(self):
        self.username_pw_set('bwyhxlso', 'Wna3huueUhrJ')
        self.connect("m21.cloudmqtt.com", 10990, 60)
        self.subscribe("$SYS/#", 0)

        rc = 0
        while rc == 0:
            rc = self.loop()
        return rc
