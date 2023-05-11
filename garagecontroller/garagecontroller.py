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

def disconnectMQTT():
     client.publish('home/garagedoor/availability',payload='offline')
     client.loop_stop()
     client.disconnect();

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
client.on_message = callback.on_message;
client.on_publish = callback.on_publish;
client.on_subscribe = callback.on_subscribe;

broker_port = int(os.getenv('port'))
broker_host = os.getenv('broker')
door_sensor_topic = os.getenv('doorsensortopic')

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
while not client.connected_flag and not client.bad_connection_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
if client.bad_connection_flag:
    client.loop_stop()    #Stop loop
    sys.exit()     
