import paho.mqtt.subscribe as subscribe
import time
import paho.mqtt.client as mqtt
import numpy as np

import serial
mqttc=mqtt.Client()
host='52.90.36.67'
ard_dire={'f':1,'l':2,'r':3,'b':4}
mqttc.connect(host,1883,60)
mqttc.loop_start()
global an
def on_message_print(client, userdata, message):
    global an
    an=(message.payload)
    print an
    client.disconnect()
def encoder(ids,direc):
    ctx=str(ids)+'||'+direc
    return ctx
def decoder(ctx):
    lis=ctx.split('|')
    return lis[0],lis[-1]
def logger(val):
    mqttc.publish("log",val, 2)
    pass

def arucoid(ide, dire):
    global an
    #print ide, dire

if __name__ =="__main__":

    while 1:
        subscribe.callback(on_message_print, "rpi3", hostname=host)
        print "received marker from cps", an
        ids, dire = decoder(an)
        #ogger('@rasp received marker {} from cps'.format(ids))

        arucoid(ids, dire)
        time.sleep(3)
        #logger('@rasp found one marker moving to next marker')
        mqttc.publish("cps3", ids, 2)
        print "sending to cps"
mqttc.loop_stop()
mqttc.disconnect()
