from machine import UART as ser
from umqtt.simple import MQTTClient
import network
import ure
sta_if = network.WLAN(network.STA_IF)
sta_if.connect('routerme', '12345678')
sta_if.ifconfig()
rfid = ser(0, 9600)
rfid.init(9600, bits=8, parity=None, stop=1)
ard=ser(1, 9600)
ard.init(9600, bits=8, parity=None, stop=1)
def main(server,val):
    c = MQTTClient("umqtt_client", server)
    c.connect()
    c.publish(b"bane", val)
    c.disconnect()
ide_lis=[b'310066832BFF', b'31006D651A23', b'3100432FE5B8', 
b'310042FBA52D', b'310046F120A6', b'3100434883B9', b'310046F2BE3B',
b'31006D69AE9B', b'310046F1199F', b'3100433C1D53', b'3100471B305D',
b'3100668313C7', b'310066830ADE',
b'3100668302D6', b'310066831DC9', b'3100668316C2',
b'3100471B375A', b'3100471B3A57', b'31006D71E0CD', b'31006D7FB497']

def ardwrite(vb):
       count=1
       for ide in ide_lis:
           if vb == str(ide):
             ard.write(str(count))
           count +=1  
       
        
while True:
      a=rfid.read()
      if a:
          b=str(a)
          ardwrite(b)
          main(server="iot.eclipse.org",val=b)
      
      
          
           


