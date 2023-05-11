import paho.mqtt.client as mqtt
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

dotenv.load_dotenv()

broker_port = int(os.getenv('port'))
broker_host = os.getenv('broker')
door_sensor_topic = os.getenv('doorSensorTopic')
power_topic = 'home/garagedoor/POWER'
state_topic = 'home/garagedoor/status'
availability_topic = 'home/garagedoor/availability'

def disconnectMQTT():
     client.publish(availability_topic,payload='offline')
     client.loop_stop()
     client.disconnect()

def on_connect(client, userdata, flags, rc, v5config=None):
    if rc==0:
        print("connected OK Returned code=",rc)
        client.subscribe(power_topic,1)
        client.subscribe(door_sensor_topic,1)
        client.publish(availability_topic,payload='online')
    else:
        print("Bad connection Returned code= ",rc)


def on_message(client, userdata, message,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Received message " + str(message.payload) + " on topic '"
        + message.topic + "' with QoS " + str(message.qos))

    if message.topic == power_topic:
          print("Single push")
          gpio.push()
    elif message.topic == door_sensor_topic:
          m_decode=str(message.payload.decode("utf-8","ignore"))
          print("data Received type",type(m_decode))
          print("data Received",m_decode)
          print("Converting from Json to Object")
          m_in=json.loads(m_decode) #decode json data
          print(type(m_in))
          print("state",m_in["contact"])
          if m_in["contact"] == True:
               client.publish(state_topic,payload='closed')
          else:
               client.publish(state_topic,payload='opened')
    
def on_publish(client, userdata, mid,tmp=None):
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Published message id: "+str(mid))
    
    
def on_subscribe(client, userdata, mid, qos,tmp=None):
    if isinstance(qos, list):
        qos_msg = str(qos[0])
    else:
        qos_msg = f"and granted QoS {qos[0]}"
    print(dt.now().strftime("%H:%M:%S.%f")[:-2] + " Subscribed " + qos_msg)    

def on_disconnect(client, userdata, rc):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True



mytransport = 'tcp' # or 'tcp'

mqtt.Client.connected_flag=False#create flag in class
mqtt.Client.bad_connection_flag=False

client = mqtt.Client(client_id="myPy",
                        transport=mytransport,
                        protocol=mqtt.MQTTv311)

client.username_pw_set(os.getenv('username'), os.getenv('password'))
client.on_connect = on_connect;
client.on_disconnect = on_disconnect;
client.on_message = on_message;
client.on_publish = on_publish;
client.on_subscribe = on_subscribe;



print('MQTT Broker: '+broker_host+':'+str(broker_port))
print('Door sensor topic: '+door_sensor_topic)

client.will_set(availability_topic,'offline',retain=False)

client.connect(broker_host,
                broker_port,
                keepalive=60,
                bind_address="")
atexit.register(disconnectMQTT)
gpio.init()

client.loop_start()
print('Running..')
while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    time.sleep(1)
if client.bad_connection_flag:
    print('Stopping..')
    client.loop_stop()    #Stop loop
    sys.exit()     
