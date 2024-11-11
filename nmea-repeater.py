#! /usr/bin/python3

import time
import paho.mqtt
import paho.mqtt.client as mqttClient
import random

from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4, dotsize=8)

lcd.clear()

##########################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe("vessels/self/navigation/position")
        client.subscribe("vessels/self/navigation/speedOverGround")

    else:
        print("Connection failed")

def on_message(client, userdata, message):
#    print("Message received : "  + str(message.payload) + " on " + message.topic)

#    if message.topic == "vessels/self/navigation/datetime":
#      data = str(message.payload.decode())
#      print(data)
#      zeta=data[11:15]
#      lcd.cursor_pos=(3,12)
#      lcd.write_string('UTC '+zeta)

    if message.topic == "vessels/self/navigation/position":
      data = str(message.payload.decode())
#          print(data)

      fields = data.split(',')
      lon = fields[0]
      lon = lon[13:20]
      lat = fields[1]
      lat = lat[11:18]
      lcd.cursor_pos=(0,0)
      lcd.write_string(lat+' N '+lon+' E')

    if message.topic == "vessels/self/navigation/speedOverGround":
      data = str(message.payload.decode())
#          print(data)
      sog=data[0:4]
#      print(sog)
      lcd.cursor_pos=(1,0)
      lcd.write_string('SOG '+sog+' kn')

    lcd.cursor_pos=(2,0)
    lcd.write_string('COG     deg')

    lcd.cursor_pos=(3,0)
    lcd.write_string('DEPTH      m')

broker_address= "localhost"
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION1, client_id)
client.on_connect= on_connect
client.on_message= on_message
client.connect(broker_address, port=port)
client.loop_start()

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
