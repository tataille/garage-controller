import paho.mqtt.client as mqtt
import callback
import os
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes 
import dotenv
import gpio

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

myport = int(os.getenv('port'))
mybroker = os.getenv('broker')
print(mybroker)


client.connect(mybroker,
                myport,
                keepalive=60,
                bind_address="");

mytopic = 'garage/push'
client.subscribe(mytopic,2);
gpio.init();
client.loop_start();