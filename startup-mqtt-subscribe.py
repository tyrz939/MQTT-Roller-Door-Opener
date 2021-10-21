import random
import time
import RPi.GPIO as GPIO
from paho.mqtt import client as mqtt_client

time.sleep(10)

broker = '192.168.40.32' # Set your server IP here
port = 1883
topic = "/shed/#"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'mqttuser'
password = 'password'

door_pin_1 = 17
door_pin_2 = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(door_pin_1, GPIO.OUT)
GPIO.setup(door_pin_2, GPIO.OUT)

GPIO.output(door_pin_1, GPIO.LOW)
GPIO.output(door_pin_2, GPIO.LOW)

# Set start time
start_time = time.time()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
         
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        
        if (time.time() - start_time) > 10:
            if msg.topic == '/shed/door1':
                GPIO.output(door_pin_1, GPIO.HIGH)
                time.sleep(0.25)
                GPIO.output(door_pin_1, GPIO.LOW)
                time.sleep(0.25)
            elif msg.topic == '/shed/door2':
                GPIO.output(door_pin_2, GPIO.HIGH)
                time.sleep(0.25)
                GPIO.output(door_pin_2, GPIO.LOW)
                time.sleep(0.25)

    client.subscribe(topic)
    client.on_message = on_message
    
    
def send():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    
def receive():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

    
receive()

