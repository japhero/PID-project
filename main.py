import rotaryio
import time
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
import digitalio
import pwmio



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

encBtn = digitalio.DigitalInOut(board.D5)
encBtn.direction = digitalio.Direction.INPUT
encBtn.pull  = digitalio.Pull.DOWN

pwm = pwmio.PWMOut(board.D11)
pwm.duty_cycle = 2 ** 15

pwm.duty_cycle = int(65355)

prevState =0
# Innitializations and global variables 


def btnControl(buttonVal ):
    global prevState
    if buttonVal and buttonVal != prevState:
        prevState = True
        return True

    elif  not buttonVal:
        prevState = False
# global Debounce function for the menu allows us to adapt to debounce several things instead of writing indidvidual debounce


class LCDPrinter: 

    def __init__(self,innitPrint,LCDObject):
        self.LCDObject = LCDObject
        self.innitPrint = innitPrint
        self.lastPrint = self.innitPrint
        # Internal variables for the class

    def print(self,UsrString):
        self.Usrinput = UsrString
        # Debounce for printing meaning more effiecent printing and cleaner lcd's
        if self.Usrinput != self.lastPrint:
            # for x in range(32):
            #     self.LCDObject.print(" ")
            # more effiecnt clearing system if needed. instead of .clear()
            self.LCDObject.clear()
            self.LCDObject.print(str(self.Usrinput))
            self.lastPrint = self.Usrinput
        

class RPMCalculator:
    # main class for getting the rpm and effiecntly printing the debug
    
    def __init__(self) -> None:
        
        self.printingDelayCounter =0
        self.lastPollingVal = False
        self.RPM = 0
        self.totalInterrupts =0
        self.time1 =0
        self.time2 =0
        #innits inside of class
        
    def debug(self,DelayInterval=500):
        if self.printingDelayCounter % DelayInterval == 1 : 
            # Location for all debug statements.
            # Better reasorce allocation  for printing debug by adding a delay to prints 
            # Doesnt mess with logic as that is seperate.
            print(f"{self.totalInterrupts} RPM: {self.RPM} btn {encBtn.value}")
    


        
            
    def RPMcompute(self):
        self.printingDelayCounter += 1
        if photoIn.value and photoIn.value != self.lastPollingVal:
            self.totalInterrupts += 1 
            self.lastPollingVal = True

            if self.totalInterrupts % 2 == 0:
                self.time1= time.monotonic()
                self.RPM = 60/((self.time1-self.time2)/5)
            
            elif self.totalInterrupts % 2 == 1:
                self.time2 = time.monotonic()
                self.RPM = 60/((self.time2-self.time1)/5)
                return self.RPM
                # takes time at first and second interupt on cycyle and takes time from first interrupt and second and 
                # gets the diffrence then devide 60 by that number to get the RPM
            
        if  not photoIn.value:
            self.lastPollingVal = False
            #debounce for photo interrupter

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
    # Seperate print statments for LCD

     
PIDon = False
while True:
    if abs(enc.position) % 2 == 0 and PIDon:
        menu(1)
        PIDon == True
        if btnControl(encBtn.value):
            PIDon = False
    elif abs(enc.position) % 2 == 0 and not PIDon:
        # Fliping PID on and OFF
        menu(2)
        PIDon = False
        if btnControl(encBtn.value):
            PIDon = True
    elif abs(enc.position) % 2 == 1 and btnControl(encBtn.value):
        enteredVal = abs(enc.position)
        while True:
            menu(4)
            RPMCalc.debug(DelayInterval=500)
            RPMCalc.RPMcompute()
            setpoint = 100*(abs(enc.position) - enteredVal)
            # internal loop if the setpoint change is entered 
            if btnControl(encBtn.value):
                break
    else:
        menu(3)
    # LCD loop manages logic of prints and then calls for prints with menu() function


    
    RPMCalc.debug(DelayInterval=500)
    RPMCalc.RPMcompute()
    # The basic RPM functions 
    
        
