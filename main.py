import rotaryio
import time
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import digitalio




lcd = digitalio.DigitalInOut(board.D8)
lcd.direction = digitalio.Direction.OUTPUT

lcd.value = False
time.sleep(.5)
lcd.value = True
i2c = board.I2C()
lcd = LCD(I2CPCF8574Interface(i2c, 0x23), num_rows=2, num_cols=16)

photoIn = digitalio.DigitalInOut(board.D10)
photoIn.direction = digitalio.Direction.INPUT
photoIn.pull  = digitalio.Pull.UP

enc = rotaryio.IncrementalEncoder(board.D7, board.D6, divisor=2)
last_position = None    

encBtn = digitalio.DigitalInOut(board.D4)
encBtn.direction = digitalio.Direction.INPUT
encBtn.pull  = digitalio.Pull.UP


prevState =0

def btnControl(buttonVal ):
    global prevState
    if buttonVal and buttonVal != prevState:
        prevState = True
        return True

    elif  not buttonVal:
        prevState = False



class LCDPrinter:

    def __init__(self,innitPrint,LCDObject):
        self.LCDObject = LCDObject
        self.innitPrint = innitPrint
        self.lastPrint = self.innitPrint


    def print(self,UsrString):
        self.Usrinput = UsrString
        #later implement system to print on multiple collums 
        if self.Usrinput != self.lastPrint:
            # for x in range(32):
            #     self.LCDObject.print(" ")
            self.LCDObject.clear()
            self.LCDObject.print(str(self.Usrinput))
            self.lastPrint = self.Usrinput
        

class RPMCalculator:
    
    def __init__(self) -> None:
        
        self.printingDelayCounter =0
        self.lastPollingVal = False
        self.RPM = 0
        self.totalInterrupts =0
        self.time1 =0
        self.time2 =0
        
    def debug(self,DelayInterval=500):
        if self.printingDelayCounter % DelayInterval == 1 :
            #all debug statements 
            print(f"{self.totalInterrupts} RPM: {self.RPM}")
    


        
            
    def RPMcompute(self):
        
        if photoIn.value and photoIn.value != self.lastPollingVal:
            self.totalInterrupts += 1 
            self.lastPollingVal = True

            if self.totalInterrupts % 2 == 0:
                self.time1= time.monotonic()
                self.RPM = 1/((self.time1-self.time2)/5)
            
            elif self.totalInterrupts % 2 == 1:
                self.time2 = time.monotonic()
                self.RPM = 1/((self.time2-self.time1)/5)
                return self.RPM
                # takes time at first and 10th interupt on cycyle and takes time from first interrupt and 10th and 
                # gets the diffrence then devide 60 by that number to get the RPM
            
        if  not photoIn.value:
            self.lastPollingVal = False

RPMCalc = RPMCalculator()

printer = LCDPrinter("innit",lcd)

setpoint =0

def menu(item):
    if item == 1:
        printer.print(f"PID \nRPM: {RPMCalc.RPM}")
    elif item == 2:
        printer.print(f"PIDOFF \nRPM: {RPMCalc.RPM}")
    elif item == 3:
        printer.print(f"ChangeSetpoint \nRPM: {RPMCalc.RPM}")
    elif item == 4:
        printer.print(f"setpoint = {setpoint}")
    

     
PIDon = False
while True:
    if abs(enc.position) % 2 == 0 and PIDon:
        menu(1)
        PIDon == True
        if btnControl(encBtn.value):
            PIDon = False
    elif abs(enc.position) % 2 == 0 and not PIDon:
        menu(2)
        PIDon = False
        if btnControl(encBtn.value):
            PIDon = True
    elif abs(enc.position) % 2 == 1 and btnControl(encBtn.value):
        enteredVal = abs(enc.position)
        while encBtn.value:
            menu(4)
            RPMCalc.printingDelayCounter += 1
            RPMCalc.debug(DelayInterval=500)
            RPMCalc.RPMcompute()
            setpoint = 100*(abs(enc.position) - enteredVal)
    else:
        menu(3)

    
    RPMCalc.printingDelayCounter += 1
    RPMCalc.debug(DelayInterval=500)
    RPMCalc.RPMcompute()
    
        
