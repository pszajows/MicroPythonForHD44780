"""
This file contains a class for manipulating LCD display based on HD44780 chip in 4-bit mode.
Currently this version supports only 16x2 LCD displays, but a simple modification of DDRAM_16char
variable may make this code working also with other sizes of displays.
See https://github.com/pszajows/MicroPythonForHD44780/edit/main/README.md for details.
"""
import machine
from time import sleep

DDRAM_16char = [0,1,0,0,0,0,0,0]
commands = {
    "clear_display":                      [0,0,0,0,0,0,0,1],
    "return_home":                        [0,0,0,0,0,0,1,0],
    "display_mode_shift_cursor_left":     [0,0,0,0,0,1,0,0],
    "display_mode_shift_cursor_right":    [0,0,0,0,0,1,1,0],
    "display_mode_shift_display_left":    [0,0,0,0,0,1,0,1],
    "display_mode_shift_display_right":   [0,0,0,0,0,1,1,1],
    "display_on_cursor_on_blink_on":      [0,0,0,0,1,1,1,1],
    "display_on_cursor_on_blink_off":     [0,0,0,0,1,1,1,0],
    "display_on_cursor_off_blink_off":    [0,0,0,0,1,1,0,0],
    "display_off_cursor_off_blink_off":   [0,0,0,0,1,0,0,0],
    "shift_display_right":                [0,0,0,1,1,1,0,0],
    "shift_cursor_right":                 [0,0,0,1,0,1,0,0],
    "shift_display_left":                 [0,0,0,1,1,0,0,0],
    "shift_cursor_left":                  [0,0,0,1,0,0,0,0],
    "4bit_2line_font10":                  [0,0,1,0,1,1,0,0],
    "4bit_2line_font7":                   [0,0,1,0,1,0,0,0],
    "set_DDRAM_address":                  [1,0,0,0,0,0,0,0]
    }


class LCD:
    def __init__(self, pins=[22,3,18,19,20,21]):
        """
        pins: this parameter contains the pin numbers, which are connected to LCD dicplay:
        pins[0] - connected to E pin of LCD display
        pins[1] - connected to RS pin of LCD display
        pins[2], pins[3], pins[4] and pins[5] - connected to D4, D5, D6 and D7 respectively
        Please note, that the RW pin of LCD display must be connected to GND and the VSS, VDD, V0, A
        and K pins need to be connected in standard way. The pins D0-D3 need no connection. 
        """
        self.E_PIN = machine.Pin(pins[0], machine.Pin.OUT)
        self.RS_PIN = machine.Pin(pins[1], machine.Pin.OUT)
        self.D_PINS = [machine.Pin(pins[2], machine.Pin.OUT),
                       machine.Pin(pins[3], machine.Pin.OUT),
                       machine.Pin(pins[4], machine.Pin.OUT),
                       machine.Pin(pins[5], machine.Pin.OUT)]

    def send4Bits(self, data4bit: list):
        self.E_PIN.value(1)
        for i in range(4):
            self.D_PINS[i].value(data4bit[3-i])
        self.E_PIN.value(0)

    def sendByte(self, databyte: list):
        self.send4Bits(databyte[:4])
        self.send4Bits(databyte[4:])
    
    def sendCommand(self, datacomm: list):
        self.RS_PIN.value(0)
        self.sendByte(datacomm)

    def sendData(self, datacomm: list):
        self.RS_PIN.value(1)
        self.sendByte(datacomm)

    def initLCD(self, mode="display_on_cursor_off_blink_off"):
        """
        Initialize LCD screen right after powering up the board.
        mode: This paramtere may take the following values:
            -"display_on_cursor_on_blink_on"
            -"display_on_cursor_on_blink_off"
            -"display_on_cursor_off_blink_off"
        """
        sleep(0.045)
        self.RS_PIN.value(0)
        self.send4Bits([0,0,1,1])
        sleep(0.005)
        self.send4Bits([0,0,1,1])
        sleep(0.0005)
        self.send4Bits([0,0,1,1])
        self.send4Bits([0,0,1,0])
        self.sendCommand(commands["4bit_2line_font7"])
        sleep(0.0001)
        self.sendCommand(commands[mode])
        sleep(0.0005)
        self.sendCommand(commands["display_mode_shift_cursor_right"])
        sleep(0.0001)
        self.sendCommand(commands["clear_display"])
    
    def setCursor(self, x: int, y: int):
        """
        Setting cursor position.
        It is assumed, that y may take only 0 and 1 values and x is also integer and stays
        between 0 and max number (-1) of columns in the display. 
        """
        command = commands["set_DDRAM_address"]
        if y==1:
            command = [i|j for (i,j) in zip(command, DDRAM_16char)]
        bx=[1 if c is '1' else 0 for c in bin(x+128)[2:]]
        bx[0]=0
        command = [i|j for (i,j) in zip(command, bx)]
        self.sendCommand(command)

    def sendText(self, text: list):
        """
        Sending text to display.
        """
        for ch in text:
            ou = [1 if c is '1' else 0 for c in bin(ord(ch)+128)[2:]]
            ou[0]=0
            self.sendData(ou)
