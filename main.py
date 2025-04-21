#from platform import machine
from machine import Pin, SoftI2C, Timer      
#from ssd1306 import SSD1306_I2C 
import urequests as requests 
import bme280
import time
#import network
#import ntptime
#import secret
#import esp32wlan
import esp32display
import mqtt
import os
#import ubinascii





#i2c_bme280 = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
i2c_bme280 = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = bme280.BME280(i2c=i2c_bme280)
mqttc = mqtt.mqttc
reconnected = 0



def readMessures(): 
  temp = bme.temperature
  hum = bme.humidity
  pres = bme.pressure
  return temp, hum, pres


def writeMessures(temp, hum, pres):
  print('Temperature: ', temp)
  print('Humidity: ', hum)
  print('Pressure: ', pres)
  esp32display.oled.fill(0)
  esp32display.textLine("Temp:  " + temp,0,0)
  esp32display.textLine("Hum:   " + hum,0,1)
  esp32display.textLine("Pres:  " + pres,0,2)
  
  esp32display.oled.show()

def sub_cb(topic, msg):
  print((topic, msg))
  #t = str(topic, encoding='utf-8')
  #print("t: ",t)
  
  if topic == b"firmware":
      time.sleep(1)
      makeResponse(topic, msg)
  elif topic == b"timer":
      getTimeDatas(msg)
  else:
      print("Topic nicht bekannt!")
      
def makeResponse(topic, msg):      
    url = msg.decode().split(",")
    print("url: ", url[0], "\nDatei: ", url[1])
    response = requests.get(url[0])
    print("status: ", response.status_code)
    if response.status_code == 200:

      with open(url[1], "w") as f:
        f.write(response.text)
        print("Update erfolgreich!")
    else:
      print("Update fehlgeschlagen!")

    response.close()

def getTimeDatas(msg): 
   print("Get Time Datas: ", msg)  

  
def publishSensors(t):
  temp, hum, pres = readMessures()
  writeMessures(temp,hum,pres)
  mqttc.publish("test", temp)
  mqttc.publish("test", hum)
  mqttc.publish("test", pres)
  mqttc.publish("innen",temp+"-"+hum+"-"+pres)
  


def connectMQTT():
  global reconnected
  reconnected=reconnected+1
  print("reconncted: ",reconnected)
  if reconnected>10:
    print("MQTT-Verbindung fehlgeschlagen!, System wird geendet!")
    exit()

  #mqttc.disconnect()
  mqttc.set_callback(sub_cb)
  mqttc.connect()
  mqttc.publish("test", "new mwssage from micropython...")
  
  mqttc.subscribe(b"firmware")
  mqttc.subscribe(b"timer")

connectMQTT()
print("Timer wird gestartet!")
timerSensors=Timer(1)
timerSensors.init(period=60000, mode=Timer.PERIODIC, callback=publishSensors)
print("Loop startet....")
print("Updated--2--!!")


while True:
    if True:
        mqttc.wait_msg()
    else:
        mqttc.check_msg()
        time.sleep(1)

mqttc.disconnect()
    
    
  