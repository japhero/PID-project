import board
from digitalio import DigitalInOut, Direction,Pull
import time

inP = DigitalInOut(board.D12)

inP.direction = Direction.INPUT
inP.pull = Pull.DOWN

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

while True:
    led.value = True
    time.sleep(1)
    led.value = False
    time.sleep(1)
    print(inP.value)