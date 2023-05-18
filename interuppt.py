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

prevState = False
startTime = float(time.monotonic())
counter = 0




interrupts =0
intTime =0
log = 0
lastVal = False

Time1 =0
time2=0
RPM =0
print("innit")
while True:
    intTime +=1


    if intTime % 250 ==1 :
    
        print(f"{interrupts} RPM: {RPM}")

    if interrupts % 10 == 0:
        time1= time.monotonic()
    elif interrupts % 10 == 9:
        time2 = time.monotonic()
        RPM = 60/((time2-time1)/5)
        # takes time at first and 10th interupt on cycyle and takes time from first interrupt and 10th and gets the diffrence then devide 60 by that number to get the RPM

    if photoIn.value and photoIn.value != lastVal:
        interrupts += 1 
        lastVal = True
    if  not photoIn.value:
        lastVal = False