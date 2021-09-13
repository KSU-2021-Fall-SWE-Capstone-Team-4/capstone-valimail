from lib.mqtt_sender import MQTTSender
from lib.mqtt_listener import MQTTListener

# Create the client
client1 = MQTTListener()
client2 = MQTTSender()

client1.subscribe('my/test/topic')

client2.publish('my/test/topic', 'HECK YEAH SON')

client1.loop_forever()
