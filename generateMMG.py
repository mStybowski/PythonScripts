import paho.mqtt.client as mqtt
import threading
import random
import json
import sys
import string


client = mqtt.Client()

try:
  ts = float(sys.argv[1])
except:
  ts = 0.5

n_packets = 20
n_channels = 8

def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_lowercase + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return(result_str)

def createData():
  data = []
  for x in range(n_packets):
    data.append(get_random_alphanumeric_string(32))
  return(data)

def printit(tmstp):
  
  tosend = wrapItUp(tmstp)

  threading.Timer(ts, printit, [tosend[1]]).start()
  client.publish("sensors/emg", tosend[0], qos=0, retain=False)
  print(tosend[0])
  print()
  print("----------------------------")
  print()

def wrapItUp(stamp):
  message = {}
  data = createData()
  message["data"] = data
  message["channels"] = n_channels
  message["packets"] = n_packets
  message["timestamp"] = stamp
  return [json.dumps(message), stamp+1]

printit(0)

client.connect("localhost", 1883, 60)
client.loop_forever()