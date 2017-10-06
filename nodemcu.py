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

ide_lis = [b'310066832BFF', b'31006D651A23', b'3100432FE5B8',
           b'310042FBA52D', b'310046F120A6', b'3100434883B9', b'310046F2BE3B',
           b'31006D69AE9B', b'310046F1199F', b'3100433C1D53', b'3100471B305D',
           b'3100668313C7', b'310066830ADE',
           b'3100668302D6', b'310066831DC9', b'3100668316C2',
           b'3100471B375A', b'3100471B3A57', b'31006D71E0CD', b'31006D7FB497']

# serial com
rfid = ser(0, 9600)
rfid.init(9600, bits=8, parity=None, stop=1)
ard = ser(1, 9600)
ard.init(9600, bits=8, parity=None, stop=1)

# mqtt configuration
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


def publ(message):
    c.publish('cps1', message)


def onMessage(topic, msg):
    global subs_temp
    print("Topic: %s, Message: %s" % (topic, msg))
    subs_temp = msg


# logging survey
def logger(val):
    c.publish("log", val)
    pass


# decryption
def decoder(ctx):
    lis = ctx.split('|')
    return lis[0], lis[-1]


def rfidtonode(rfid):
    count = 0
    logger('@rasp {}'.format(rfid))
    for ide in ide_lis:

        if rfid == str(ide):
            ard.write(str(count))
            break
        count += 1
    return count-1


def action(ids, dire, flag):
    time.sleep(2)
    logger('@rasp reached the function {}'.format(dire))

    while flag:
        # checking for the rfid input
        while 1:
            line = rfid.read()
            if line:
                logger('@rasp READ MARKER ID')
                break

        node = rfidtonode(line)
        time.sleep(2)
        logger('@rasp found node {}'.format(node))

        '''logic'''
        count=3
        if dire=="s'":
            pass

        if dire== "u'":
            ard.write(str(count))
        if dire=="d'":
            pass
        if dire=="f'":
            pass
        if dire=="r'":
            pass
        flag = False

    pass


if __name__ == '__main__':
    logger('robot is online')
    time.sleep(2)
    client = MQTTClient(CONFIG['CLIENT_ID'], CONFIG['MQTT_BROKER'], user=CONFIG['USER'], password=CONFIG['PASSWORD'],
                        port=CONFIG['PORT'])

    client.connect()
    client.set_callback(onMessage)
    client.subscribe(b'rpi1')
    time.sleep(2)

    while 1:
        client.wait_msg()
        logger(subs_temp)
        ids, dire = decoder(str(subs_temp))
        time.sleep(2)
        logger('@rasp received marker {} from cps'.format(ids))
        action(ids=ids, dire=dire, flag=True)
        logger('@rasp operation done')
        publ(ids)

    c.disconnect()
