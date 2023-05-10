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
     client.loop_stop()
     client.disconnect();

dotenv.load_dotenv()


mytransport = 'tcp' # or 'tcp'

client = mqtt.Client(client_id="myPy",
                        transport=mytransport,
                        protocol=mqtt.MQTTv311)

client.username_pw_set(os.getenv('username'), os.getenv('password'))
client.on_connect = callback.on_connect;
client.on_message = callback.on_message;
client.on_publish = callback.on_publish;
client.on_subscribe = callback.on_subscribe;

broker_port = int(os.getenv('port'))
broker_host = os.getenv('broker')
door_sensor_topic = os.getenv('doorsensortopic')

print('MQTT Broker: '+broker_host+':'+broker_port)
print('Door sensor topic: '+door_sensor_topic)

client.will_set('home/garagedoor/availability','offline',retain=False)

client.connect(broker_host,
                broker_port,
                keepalive=60,
                bind_address="")
atexit.register(disconnectMQTT)
gpio.init()

client.publish('home/garagedoor/availability',payload='online')
client.loop_forever()
     
