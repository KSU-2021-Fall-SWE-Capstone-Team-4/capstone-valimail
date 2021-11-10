from lib.mqtt_sender import MQTTSender
from lib.mqtt_listener import MQTTListener
from time import sleep
from dotenv import load_dotenv
load_dotenv(verbose=True)

# First things first, launch the logger.
from lib.util import logger
logger.basic_setup()

# Create the client
client2 = MQTTSender()
client2.publish(payload='{"payload":"SGVsbG8gV29ybGQ","protected":"eyJhbGciOiJSUzI1NiIsIng1dSI6ImRuczovL2tzdS5fZGV2aWNlLnVuaXZlcnNhbGF1dGguY29tP3R5cGU9VExTQSJ9","signature":"YWXJpSG3yUjPu0ipkHInbILzYo2Hy2dbz2hsECzhUVMeGEHeUT4bLFf0w8zYtt9LEekadGTbsxD-8Zb3N5YJEdJVc3L9mmbMcaftxllphps1lZ4q1LH8JzlUtdroj2GkTagVU-uA-S4Yzf964b7HJ2mezc4Ua2dYMVnNJfUhm2je9j4PhCkO9kROT8MU7U6FbY6obWDPUgx94sCw9LI934MIEo-GUvCBc08zlHnneNH2vni1zDV9P4_pgoTyGE_uXMTMnsDIVB0cluklPKD4p1ZtOob0p9oCrJ7L2lJFjEP3-GJ5Qs2s9NqapFEVhz4PohOiucJlKVZesY0nNbMgvw"}')

sleep(60)

