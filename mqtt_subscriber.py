
import paho.mqtt.client as mqtt
import time
import serial
import json

#pyserial setup copied from Gemini
ser =  serial.Serial("/dev/ttyACM0", 115200, timeout=1, write_timeout=1, rtscts=False, dsrdtr=False, xonxoff=False)
time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("dwm/node/+/uplink/location", 1)])


def on_message(client, userdata, message):
    #formatting code copied from Gemini
	print("got message on {}".format(message.topic), flush = True)
	try:	
		raw_str = message.payload.decode('utf-8')
		data = json.loads(raw_str)
		x = data['position']['x']
		y = data['position']['y']

		# print("Message received: " + message.topic + " : " + str(message.payload))
		node_id = message.topic.split('/')[2]
		format_out = "node_id = {}, x = {}, y = {};\n".format(node_id, x, y)
		print(format_out)
		ser.write(format_out.encode('utf-8'))    
# if message.topic == 'ep_mqtt/topic2':
        # with open('/home/pi/mqtt_update.txt', 'a+') as f:
            # f.write("received topic2")
	except Exception as e:
		print("Error formatting: {}".format(e))
broker_address = "localhost"  # Broker address
port = 1883  # Broker port
# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
