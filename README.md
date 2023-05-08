# mqtt-garage-controller

Python projet Allow to allow to control garage door through MQTT.

## Garage Door & Motor

- Manufacturer : Normsthal
- Motor Model : Ultra
- RJ9 - red / green
- Zigbee door contactor

## MQTT topics



## Home Assistant

```mqtt

command_topic: "home/garagedoor/POWER"
state_topic: "home/garagedoor/status"
availability_topic: "home/garagedoor/availability"    
payload_available: "online"
payload_not_available: "offline"
payload_open: "ON"
payload_close: "ON"
payload_stop: "ON"
state_open: "opened"
state_closed: "closed"
```



