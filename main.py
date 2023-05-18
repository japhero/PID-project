import rotaryio
import time
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import digitalio

lcd = digitalio.DigitalInOut(board.D8)
lcd.direction = digitalio.Direction.OUTPUT

# lcd.value = False
# time.sleep(.5)
lcd.value = True
i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x23), num_rows=2, num_cols=16)



enc = rotaryio.IncrementalEncoder(board.D7, board.D6,2)
last_position = None

encBtn = digitalio.DigitalInOut(board.D4)
encbtn = digitalio.Direction.INPUT
encbtn  = digitalio.Pull.DOWN

prevState =0

def btnControl(buttonVal ):
    global prevState
    if buttonVal and buttonVal != prevState:
        prevState = True

    elif  not buttonVal:
        prevState = False

def menu(item):
    if item == 1:
        print("menu one")
    elif item == 3:
        print("case 2")
    elif item == 3:
        print("case 3 ")

     
        

def retEnc(x):
    array = ["PID","No PID","Setpoint"] 
    output = x%3
    btnControl(encBtn.value,output)
    return array[output]


class LCDPrinter:

    def __init__(self,innitPrint,LCDObject):
        self.LCDObject = LCDObject
        self.innitPrint = innitPrint
        self.lastPrint = self.innitPrint


    def print(self,UsrString):
        self.Usrinput = UsrString
        #later implement system to print on multiple collums 
        if self.Usrinput != self.lastPrint:
            for x in range(15):
                self.LCDObject.print(" ")
            self.LCDObject.print(str(self.Usrinput))
            self.lastPrint = self.Usrinput
        


printer = LCDPrinter("innit",lcd)


while True:
    printer.print("hello world")
    print(menu(3))
    print(f" {enc.position} {encBtn.value}")
        
