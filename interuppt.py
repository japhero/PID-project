import time
import board
import digitalio
import analogio
import pwmio


photoIn = digitalio.DigitalInOut(board.D10)
photoIn.direction = digitalio.Direction.INPUT
photoIn.pull  = digitalio.Pull.UP


pwm = pwmio.PWMOut(board.D11)
pwm.duty_cycle = 2 ** 15

pwm.duty_cycle = int(65355)

print("innit")

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
    
    def RpmCompute(self):
        

        if self.totalInterrupts % 5 == 0:
            self.time1= time.monotonic()
            self.RPM = 1/((self.time1-self.time2)/5)
            
        elif self.totalInterrupts % 5 == 4:
            self.time2 = time.monotonic()
            self.RPM = 1/((self.time2-self.time1)/5)
            return self.RPM
            # takes time at first and 10th interupt on cycyle and takes time from first interrupt and 10th and 
            # gets the diffrence then devide 60 by that number to get the RPM
            
    def pollingForInterrupts(self):
        
        if photoIn.value and photoIn.value != self.lastPollingVal:
            self.totalInterrupts += 1 
            self.lastPollingVal = True
            
        if  not photoIn.value:
            self.lastPollingVal = False

RPMCalc = RPMCalculator()

while True:


    time.sleep(.0001)
    RPMCalc.printingDelayCounter += 1
    RPMCalc.debug(DelayInterval=500)
    RPMCalc.RpmCompute()
    RPMCalc.pollingForInterrupts()
    