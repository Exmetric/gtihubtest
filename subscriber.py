import paho.mqtt.client as mqtt

import json



# Callback when the client receives a message from the broker

def on_message(client, userdata, msg):

try:

# Decode the JSON payload

message = msg.payload.decode("utf-8")

data = json.loads(message) # Convert the JSON string back to a Python dict

print(f"Received data: {data}")



# Access the distance value

print(f"Distance: {data['distance']} cm")



except json.JSONDecodeError:

print("Failed to decode JSON message")

except KeyError as e:

print(f"Missing expected key: {e}")



# Callback when the client connects to the broker

def on_connect(client, userdata, flags, rc):

print("Connected with result code " + str(rc))

# Subscribe to the topic when connected

client.subscribe("sensors/ultrasonic")



# MQTT setup

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message



# Connect to the broker

client.connect("test.mosquitto.org", 1883, 60)



# Start the loop to process network traffic and dispatch callbacks

client.loop_forever()