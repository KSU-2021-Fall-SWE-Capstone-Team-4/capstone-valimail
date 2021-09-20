from lib.mqtt_sender import MQTTSender
from lib.mqtt_listener import MQTTListener
from time import sleep

# Create the client
client2 = MQTTSender()

client2.publish('my/test/topic', 'HECK YEAH SON')

sleep(60)