import time
import paho.mqtt.client as mqtt

mqttc=mqtt.Client()
mqttc.connect("localhost",1883,60)
mqttc.loop_start()
a = 1
while 1:
    a = a + 1
    mqttc.publish("rob",a,2)
    time.sleep(1)
    print a

mqttc.loop_stop()
mqttc.disconnect()
