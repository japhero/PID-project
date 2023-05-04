import rotaryio
import time
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import digitalio

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

led.value = True

i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x27), num_rows=2, num_cols=16)



enc = rotaryio.IncrementalEncoder(board.D9, board.D10,2)
last_position = None

encBtn = digitalio.DigitalInOut(board.D11)
encbtn = digitalio.Direction.INPUT
encbtn  = digitalio.Pull.UP

prevState =0

def btnControl(buttonVal ,out):
    global prevState
    if buttonVal and buttonVal != prevState:
        prevState = True
        if out == 0:
            print("PID           ACTIVE")
        elif out == 1:
            print("No PID        INACTVE")
    elif  not buttonVal:
        prevState = False
     
        

def retEnc(x):
    array = ["PID","No PID"] 
    output = x%2
    btnControl(encBtn.value,output)
    return array[output]




while True:
    lcd.print(retEnc(enc.position))
    time.sleep(.001)
    lcd.clear()
    print(f"{retEnc(enc.position)} {enc.position} {encBtn.value}")
        
