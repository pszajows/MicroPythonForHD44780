from hd44780 import LCD

"""
Example, how to use HD44780-based LCD display with Raspberry Pi Pico.
"""

lcd = LCD()
lcd.initLCD()
lcd.setCursor(0,0)
lcd.sendText("Hello, ")
lcd.setCursor(0,1)
lcd.sendText("World!")

