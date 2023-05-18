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
print("innit")
while True:
    intTime +=1


    if intTime % 250 ==1 :
    
        print(f"{interrupts} ")

    if photoIn.value and photoIn.value != lastVal:
        interrupts += 1 
        lastVal = True
    if  not photoIn.value:
        lastVal = False