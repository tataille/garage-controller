import paho.mqtt.client as mqtt
import callback
import os
import time
import atexit
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import dotenv
import gpio
import sys
from datetime import datetime as dt
from paho.mqtt.client import connack_string as ack
import json

def disconnectMQTT():
     client.publish('home/garagedoor/availability',payload='offline')
     client.loop_stop()
     client.disconnect();



def on_connect(client, userdata, flags, rc, v5config=None):
    if rc==0:
        print("connected OK Returned code=",rc)
        mytopic = 'home/garagedoor/POWER'
        client.subscribe(mytopic,2);  
    else:
        print("Bad connection Returned code= ",rc)


def on_message(client, userdata, message,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    if message.topic ==
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

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.bad_connection_flag=True

def on_disconnect(client, userdata, rc):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

dotenv.load_dotenv()


mytransport = 'tcp' # or 'tcp'

mqtt.Client.connected_flag=False#create flag in class

client = mqtt.Client(client_id="myPy",
                        transport=mytransport,
                        protocol=mqtt.MQTTv311)

client.username_pw_set(os.getenv('username'), os.getenv('password'))
client.on_connect = on_connect;
client.on_disconnect = on_disconnect;
client.on_message = on_message;
client.on_publish = on_publish;
client.on_subscribe = on_subscribe;

broker_port = int(os.getenv('port'))
broker_host = os.getenv('broker')
door_sensor_topic = os.getenv('doorSensorTopic')

print('MQTT Broker: '+broker_host+':'+str(broker_port))
print('Door sensor topic: '+door_sensor_topic)

client.will_set('home/garagedoor/availability','offline',retain=False)

client.connect(broker_host,
                broker_port,
                keepalive=60,
                bind_address="")
atexit.register(disconnectMQTT)
gpio.init()

client.publish('home/garagedoor/availability',payload='online')
client.subscribe(door_sensor_topic,1)
while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()     
