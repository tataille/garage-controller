# mqtt-garage-controller

Python projet to allow to control garage door through MQTT.

## Garage Door & Motor

- Manufacturer : Normsthal
- Motor Model : Ultra
- RJ9 - red / green
- Zigbee door contactor

## MQTT topics

## Home Assistant

```mqtt
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

## Configuration

Create a .env file into root directory.

```bash
broker=mosquitto_ip
port=mosquitto_port
username=mosquitto_account
password=mosquitto_password
doorSensorTopic=zigbee2mqtt/0xxxxxxxxxxxxxxx
```

## services

```bash
sudo systemctl enable /home/pi/git/mqtt-garage-controller/service/wifi-control-led.service
sudo systemctl enable /home/pi/git/mqtt-garage-controller/service/garage-controller.service
```
