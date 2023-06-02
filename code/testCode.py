
import time

time1=0
time2=0
RPM =0

for totalInterrupts in range(8):
    time.sleep(1)
    print(f"RPM: {RPM} T1: {time1} T2: {time2} mod {totalInterrupts %2} X {totalInterrupts}")

    if totalInterrupts % 2 == 0:
        time1= time.monotonic()
        RPM = 60/((time1-time2))

    elif totalInterrupts % 2 == 1:
        time2 = time.monotonic()
        RPM = 60/((time2-time1))
    