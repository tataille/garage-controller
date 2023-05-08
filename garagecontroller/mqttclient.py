import paho.mqtt.client as mqtt
import callback
import os
import time
import atexit
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import dotenv
import gpio

def disconnectMQTT():
     client.publish('home/garagedoor/availability',payload='offline')
     client.disconnect();

dotenv.load_dotenv()


mytransport = 'tcp' # or 'tcp'


client = mqtt.Client(client_id="myPy",
                        transport=mytransport,
                        protocol=mqtt.MQTTv311)
client.connected_flag=False

client.username_pw_set(os.getenv('username'), os.getenv('password'))
client.on_connect = callback.on_connect;
client.on_message = callback.on_message;
client.on_publish = callback.on_publish;
client.on_subscribe = callback.on_subscribe;

myport = int(os.getenv('port'))
mybroker = os.getenv('broker')
print(mybroker)


client.connect(mybroker,
                myport,
                keepalive=60,
                bind_address="")

atexit.register(disconnectMQTT)
gpio.init()

while not client.connected_flag: #wait in loop
     time.sleep(1)
     
client.publish('home/garagedoor/availability',payload='online')
