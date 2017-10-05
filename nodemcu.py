import network
from umqtt.simple import MQTTClient
from machine import Pin
import machine
import ubinascii
from machine import UART as ser
import time

#network establishment
sta_if = network.WLAN(network.STA_IF)
sta_if.connect('routerme', '12345678')
sta_if.active()
sta_if.ifconfig()
subs_temp=''

#serial com
rfid = ser(0, 9600)
rfid.init(9600, bits=8, parity=None, stop=1)
ard=ser(1, 9600)
ard.init(9600, bits=8, parity=None, stop=1)





#mqtt configuration
CONFIG = {
     # Configuration details of the MQTT broker
     "MQTT_BROKER": "iot.eclipse.org",
     "USER": "",
     "PASSWORD": "",
     "PORT": 1883,
     "TOPIC": b"test",
     # unique identifier of the chip
     "CLIENT_ID": b"esp8266_" + ubinascii.hexlify(machine.unique_id())}
c = MQTTClient("umqtt_client", CONFIG['MQTT_BROKER'])

c.connect()




def publish(message):
    c.publish('cps1', message)


def onMessage(topic, msg):
    global subs_temp
    print("Topic: %s, Message: %s" % (topic, msg))
    subs_temp=msg

#logging survey
def logger(val):
    c.publish("log",val)
    pass

#decryption
def decoder(ctx):
    lis=ctx.split('|')
    return lis[0],lis[-1]

if __name__=='__main__':
    logger('robot is online')
    time.sleep(2)
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'], port=CONFIG['PORT'])

    client.connect()
    client.set_callback(onMessage)
    client.subscribe(b'rpi1')
    time.sleep(2)
    
    logger('subscription over')
    
    while 1:
        time.sleep(2)
        logger('entered loop')
        client.wait_msg()
        time.sleep(2)
        logger(subs_temp)
        ids, dire = decoder(str(subs_temp))
        time.sleep(2)
        logger('@rasp received marker {} from cps'.format(ids))
        

    c.disconnect()