from machine import Pin, I2C      
from ssd1306 import SSD1306_I2C  

i2c_oled = I2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(128,64,i2c_oled)



def textLine(text, col = 0, row = 0): 
  x = 10 * col
  y = 11 * row
  oled.text(text, x, y)