import paho.mqtt.subscribe as subscribe


def on_message_print(client, userdata, message):
    a= (message.payload)
    print a
    with open("loge.txt", "a") as log_file:
        log_file.write('{}\n'.format(a))

    client.disconnect()

with open('loge.txt','w'): pass
while 1:
    subscribe.callback(on_message_print, "log", hostname='52.90.36.67')