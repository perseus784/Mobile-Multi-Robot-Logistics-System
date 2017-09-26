import paho.mqtt.subscribe as subscribe
import time,csv
import paho.mqtt.client as mqtt
import numpy as np
import serial

mqttc=mqtt.Client()
host='52.90.36.67'
ard_dire={'u':1,'l':2,'r':3,'d':4}
port = '/dev/ttyS0'
ard = serial.Serial(port,9600,timeout=5)
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

def csvfunc(line):
    endlist = []
    with open('rpiref.csv', 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter='|')
        for row in spamreader:
            if row['node'] == line:
                endlist.append(row['markerid'])
    return endlist

def decoder(ctx):
    lis=ctx.split('|')
    return lis[0],lis[-1]

def logger(val):
    mqttc.publish("log",val, 2)
    pass

prev = ''

def arucoid(ide, dire,flag):
    global an
    global prev
    print ide, dire

    while flag:
        line = ard.read(12)  # read a '\n' terminated line
        # print line
        line1 = csvfunc(line)
        if str(ide)==str(line1):
            logger('@rasp found marker id {}'.format(ide))
            if dire=='r' or 'l':

                #make turn
                ard.write(str(ard_dire[dire]))
                logger('@arduino sent to arduino')
                time.sleep(2)
                msg = ard.readline(ard.inWaiting())
                #go forward
                ard.write(str(1))
                logger('@arduino sent to arduino')
                time.sleep(2)
                msg = ard.readline(ard.inWaiting())
            elif dire=='d':
                if prev != 'd':
                    ard.write(str(ard_dire[dire]))
                    logger('@arduino sent to arduino')
                    time.sleep(2)
                    msg = ard.readline(ard.inWaiting())
                else:
                    prev ='d'
                    ard.write(str(1))
                    logger('@arduino sent to arduino')
                    time.sleep(2)
                    msg = ard.readline(ard.inWaiting())
            elif dire=='u':
                ard.write(str(ard_dire[dire]))
                logger('@arduino sent to arduino')
                time.sleep(2)
                msg = ard.readline(ard.inWaiting())

            flag = False

if __name__ =="__main__":
    logger('@rasp sucessfully launched robot')

    while 1:
        subscribe.callback(on_message_print, "rpi1", hostname=host)
        print "received marker from cps", an
        ids, dire = decoder(an)
        logger('@rasp received marker {} from cps'.format(ids))

        arucoid(ids, dire,flag=True)
        time.sleep(3)
        logger('@rasp found one marker moving to next marker')
        mqttc.publish("cps1", ids, 2)
        print "sending to cps"

mqttc.loop_stop()
mqttc.disconnect()
