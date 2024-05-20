from machine import Pin, SoftI2C      
#from ssd1306 import SSD1306_I2C  
import bme280
import time
#import network
#import ntptime
#import secret
#import esp32wlan
import esp32display
import mqtt





#i2c_bme280 = I2C(scl=Pin(22), sda=Pin(21), freq=10000)
i2c_bme280 = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
bme = bme280.BME280(i2c=i2c_bme280)



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


#esp32wlan.wifi.do_connect()

mqttc = mqtt.mqttc
mqttc.connect()
mqttc.publish("test", "new mwssage from micropython...")


while True:
  temp, hum, pres = readMessures()
  writeMessures(temp,hum,pres)
  mqttc.publish("test", temp)
  mqttc.publish("test", hum)
  mqttc.publish("test", pres)
  mqttc.publish("innen",temp+"-"+hum+"-"+pres)
  time.sleep(10)