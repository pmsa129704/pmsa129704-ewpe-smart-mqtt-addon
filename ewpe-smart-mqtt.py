import paho.mqtt.client as mqtt
import yaml
import time
import socket
import json
import threading

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

mqtt_config = config['mqtt']
devices = config['devices']

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(mqtt_config['user'], mqtt_config['password'])
mqtt_client.connect(mqtt_config['broker'], mqtt_config['port'], 60)
mqtt_client.loop_start()

def listen_device(device):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((device['ip'], device['port']))
    while True:
        data = s.recv(1024)
        if data:
            topic = f"{mqtt_config['topic_prefix']}/{device['name']}/status"
            mqtt_client.publish(topic, data.hex())
        time.sleep(1)

for device in devices:
    t = threading.Thread(target=listen_device, args=(device,))
    t.start()

while True:
    time.sleep(60)
