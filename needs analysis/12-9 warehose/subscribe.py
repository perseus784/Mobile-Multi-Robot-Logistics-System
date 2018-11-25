import paho.mqtt.subscribe as subscribe

def on_message_print(client, userdata, message):
    print("%s " %(message.payload))
    client.disconnect()
while 1:
    
    subscribe.callback(on_message_print, "rob", hostname="localhost")
    print "yeah"
