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
        
    def debug(self,DelayInterval=500):
        if self.printingDelayCounter % DelayInterval == 1 :
            #all debug statements 
            print(f"{self.totalInterrupts} RPM: {self.RPM}")
    
    def RpmCompute(self):
        
        if self.totalInterrupts % 10 == 0:
            self.time1= time.monotonic()
            
        elif self.totalInterrupts % 10 == 9:
            self.time2 = time.monotonic()
            self.RPM = 60/((self.time2-self.time1)/5)
            return self.RPM
            # takes time at first and 10th interupt on cycyle and takes time from first interrupt and 10th and 
            # gets the diffrence then devide 60 by that number to get the RPM
            
    def pollingForInterrupts(self):
        
        if photoIn.value and photoIn.value != self.lastPollingVal:
            self.totalInterrupts += 1 
            self.lastPollingVal = True
            
        if  not photoIn.value:
            self.lastPollingVal = False

RPMCalculator1 = RPMCalculator()

while True:



    RPMCalculator1.printingDelayCounter += 1
    RPMCalculator1.debug(DelayInterval=500)
    RPMCalculator1.RpmCompute()
    RPMCalculator1.pollingForInterrupts()
    