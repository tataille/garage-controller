from datetime import datetime as dt
from paho.mqtt.client import connack_string as ack
import json
import gpio


def on_connect(client, userdata, flags, rc, v5config=None):
    if rc==0:
        print("connected OK Returned code=",rc)
        mytopic = 'garage/push'
        client.subscribe(mytopic,2);  
    else:
        print("Bad connection Returned code= ",rc)


def on_message(client, userdata, message,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    print("Single push")
    gpio.push()
    
def on_publish(client, userdata, mid,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))
    
def on_subscribe(client, userdata, mid, qos,tmp=None):
    if isinstance(qos, list):
        qos_msg = str(qos[0])
    else:
        qos_msg = f"and granted QoS {qos[0]}"
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Subscribed " + qos_msg)    