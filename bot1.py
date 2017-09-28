import paho.mqtt.subscribe as subscribe
import time,csv
import paho.mqtt.client as mqtt
import numpy as np
import serial

mqttc=mqtt.Client()
host='52.90.36.67'
ard_dire={'s':0,'u':1,'l':2,'r':3,'d':4}
port = '/dev/ttyACM0'
ard = serial.Serial(port,9600,timeout=5)
ser= serial.Serial('/dev/ttyS0',9600,timeout=5)
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

prevd = ''
prevr = ''
prevl = ''
previousid=''
def arucoid(ide, dire,flag):
    global an
    global previousid
    global prevd,prevl,prevr
    print ide, dire
    logger('@rasp {}reached the function'.format(ide))
    #ard.write(str(ard_dire['u']))
    while flag:

        while 1:
            line = ser.read(12)
            if line:
                logger('@rasp found marker id')
                break

        # print line
        line1 = csvfunc(line)
        print 'line',line1
        ard.write(str(ard_dire['s']))

        if str(ide)==str(line1[0]):
            print 'here'
            logger('@rasp FOUND marker id {}'.format(ide))
            if dire=='s':
                break
            if dire==('r' or 'l'):
                if dire != (prevl or prevr):
                    # make turn
                    ard.write(str(ard_dire[dire]))
                    logger('@arduino sent to arduino')
                    time.sleep(2)
                    msg = ser.readline(ard.inWaiting())
                    # go forward
                    ard.write(str(1))
                    logger('@arduino sent to arduino')
                    time.sleep(2)
                    msg = ser.readline(ard.inWaiting())
                else:
                    if dire=='r':prevr='r'
                    elif dire=='l':prevl='l'
                    ard.write(str(1))
                    logger('@arduino sent to arduino')
                    msg = ser.readline(ard.inWaiting())

            elif dire=='d':
                if prevd != 'd':
                    ard.write(str(ard_dire['l']))
                    time.sleep(3)
                    ard.write(str(ard_dire['l']))
                    logger('@arduino sent to arduino')
                    msg = ser.readline(ard.inWaiting())
                else:
                    prevd ='d'
                    ard.write(str(1))
                    logger('@arduino sent to arduino')
                    time.sleep(2)
                    msg = ser.readline(ard.inWaiting())

            elif dire=='u':
                ard.write(str(ard_dire[dire]))
                logger('@arduino sent to arduino')
                msg = ser.readline(ard.inWaiting())
            flag = False

if __name__ =="__main__":
    logger('@rasp sucessfully launched robot')

    while 1:
        subscribe.callback(on_message_print, "rpi1", hostname=host)
        print "received marker from cps", an
        ids, dire = decoder(an)
        logger('@rasp received marker {} from cps'.format(ids))

        arucoid(ids, dire,flag=True)
        ard.write(str(ard_dire['s']))
        logger('@rasp found one marker moving to next marker')
        mqttc.publish("cps1", ids, 2)
        print "sending to cps"

mqttc.loop_stop()
mqttc.disconnect()
