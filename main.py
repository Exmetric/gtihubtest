import RPi.GPIO as GPIO

import time

import paho.mqtt.client as mqtt

import json



# Set the GPIO mode

GPIO.setmode(GPIO.BCM)



# Define GPIO pin for the sensor signal (Trig + Echo combined)

signal_pin = 5



# Set up the GPIO pin initially as output for the trigger

GPIO.setup(signal_pin, GPIO.OUT)



# Function to get the distance from the ultrasonic sensor

def get_distance():

# Ensure pin is set to output mode (to send the trigger pulse)

GPIO.setup(signal_pin, GPIO.OUT)



# Send a 10µs pulse to trigger the sensor

GPIO.output(signal_pin, True)

time.sleep(0.00001) # 10 microseconds

GPIO.output(signal_pin, False)



# Change the pin mode to input to read the echo

GPIO.setup(signal_pin, GPIO.IN)



# Wait for the echo to start (signal pin goes HIGH)

start_time = time.time()

while GPIO.input(signal_pin) == 0:

start_time = time.time()



# Wait for the echo to end (signal pin goes LOW)

stop_time = time.time()

while GPIO.input(signal_pin) == 1:

stop_time = time.time()



# Calculate the time difference

time_elapsed = stop_time - start_time



# Calculate the distance based on the speed of sound (34300 cm/s)

distance = (time_elapsed * 34300) / 2



return distance



def publish():

# Initialize the MQTT client

client = mqtt.Client()

client.connect("test.mosquitto.org", 1883, 60)



while True:

# Get distance data

distance = get_distance()



# Create JSON payload with distance

data = {

"distance": distance

}



# Convert data to JSON string

json_data = json.dumps(data)



# Publish the data to the broker

client.publish("sensors/ultrasonic", json_data)

print(f"Published: {json_data}")



time.sleep(2) # Publish every 5 seconds



if __name__ == "__main__":

try:

publish()

except KeyboardInterrupt:

GPIO.cleanup() # Clean up GPIO when exiting