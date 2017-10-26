import network
from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
from machine import UART as ser
import time

# network establishment
sta_if = network.WLAN(network.STA_IF)
sta_if.connect('routerme', '12345678')
sta_if.active()
time.sleep(2)
sta_if.ifconfig()
subs_temp = ''


# mqtt configuration
CONFIG = {
    # Configuration details of the MQTT broker
    "MQTT_BROKER": "iot.eclipse.org",
    "USER": "",
    "PASSWORD": "",
    "PORT": 1883,
    "TOPIC": "test",
    # unique identifier of the chip
    "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())}
c = MQTTClient("umqtt_client", CONFIG['MQTT_BROKER'])
c.connect()


def publ(message):
    c.publish('donot', message)


def onMessage(topic, msg):
    global subs_temp
    print("Topic: %s, Message: %s" % (topic, msg))
    subs_temp = msg


if __name__ == '__main__':

    time.sleep(2)
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'],
                        port=CONFIG['PORT'])

    client.connect()
    client.set_callback(onMessage)
    publ(ids)
    c.disconnect()
