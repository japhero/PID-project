# PID-project



# WIRING
ROT ENCODER (CLK, 9) (DT, 10) (SW, 11)
PHOTO INT (IN, 7)
SERVO (IN, 13)

<img src="https://i.stack.imgur.com/AjURy.png" alt="enter image description here">
https://electronics.stackexchange.com/questions/179084/driving-dc-motor-using-a-single-mosfet-why-does-the-motor-spin-without-applying 


This is the explanation for individual code segments and ideas for future reference and for grading of the PID assignment 



## RPM computation
The RPM computation is the system which takes the Rotations per minute and also manages the overall debug functions to efficiently allow consistent output.

### Initial development Problems
The first solutions and the problems with those solutions
* ASYNCIO was a solution that was put on the table but seemed to be a way to simulate the asynchronous ability that interrupts gave us. This however didn't seem to be plausible as the Library would be to difficult to use in the short time frame that we had and would force us to have everything in classes as to keep persistent variables making the code much harder to write and much more complicated.
* Polling was the second option and the currently implemented solution. Polling is just checking the pin for a constant cycle and updating variables on the change in that pin. This differs with interrupts as the program doesn't stop and run the interrupt loop as soon as the interrupt pin is triggered. This causes problems as if the value is switching faster than the program loop than it simply will skip that input.

### Code analysis and explanation

```python
def RPMcompute(self):
        
        if photoIn.value and photoIn.value != self.lastPollingVal:
            self.totalInterrupts += 1 
            self.lastPollingVal = True

            if self.totalInterrupts % 2 == 0:
                self.time1= time.monotonic()
                self.RPM = 1/((self.time1-self.time2))
            
            elif self.totalInterrupts % 2 == 1:
                self.time2 = time.monotonic()
	            self.RPM = 60/((self.time2-self.time1))
                return self.RPM
                
        if  not photoIn.value:
            self.lastPollingVal = False

```
>Code of the compute function in the RPMCalculator class.

## Approach
We approach the problem of calculating rpm by getting 2 time variables one at the first interrupt of the Circle (2 Interrupts per full rotation)  and one at the second interrupt. then we subtract the second by the first to get the difference then on the next cycle we just subtract inversely doing the now "first" but actually second minus the now second. The way that we easily maintain a loop of number is the Modulo operator (<span style="color:orange"> %</span> ) which just divides by a set number and the returns the remainder of that division.  This is very useful when it comes to controlling loops as it sets a forever infinitely increasing number to forever repeat at an interval of <span style = color:lightgreen > 0 until N-1 </span> that's also how we treat the RPM calculations as seen in the code we take an MOD 2 of the total interrupts and therefore can easily forever split the increasing number of interrupts into groups of 0 and 1 as every even interrupt will be 0 and every odd will be 1 giving us the opportunity to get the times and preform the calculations 

<img src = "https://i.imgur.com/rEf0TpX.png" width =400>
> The graphic is an example of how rpm would be computed for the first for interrupts.

#### Calculation

``` python
RPM = 60/((self.time2-self.time1))
```
![](https://i.imgur.com/743DyXs.png)

The calculation is just taking the time between the interrupt second interrupt/A full rotation - the time of the last full rotation. You may ask why wouldn't you just get the time at full rotation this is because of the function used Monatomic time is a set point of time not a sort of stopwatch, therefore we can't just call it and assume the timer started on the first interrupt for example if want the time in between 8am and 10am we would take 10 and subtract 8.

## Printing to the LCD
The printing wasn't really A problem, butt more of a QOL decision I made to improve the look and let the system use the resources more efficiently to accommodate for the polling.

``` python
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
```

This is the function for printing, all it really is a debounce for strings(words). This allows the metro/computer to not constantly have to send clear commands to the LCD as to not stack words forever.

## LCD Menu
The LCD menu is a system of messages on the LCD that change based on the rotary encoder and its button. These messages let the user control the activation of PID and the set point. The two menu options are "PID state" and "Change Set point" these change with the scroll weel and then the action is done when the button is pressed.

![[Screenshot 2023-05-30 153423.png|300]]
This flowchart shows the options of the LCD the 2 scroll options are at the top and then the action flowchart is below.



### Iterations
* The first iteration was a Tkinter window because i had not set up the LCD for debugging, yet the system was "FrankenCode"Spaghetti code and a very legacy approach using Modulo to loop over a list of strings that were then printed to the LCD. The problem was the fact that it was hard to enter an individual item/tree.
* The second and final Iteration is one where we separate prints into different commands on a menu function and then to change the LCD we just call different values on that menu function. This allows separation between the logic of the menu and the actual printing, making the code much easier to understand and write, as one system is independent of another.

### Code explanation 

``` python
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
    
        
```

#### Scrolling
Because there are 2 options, therefore we will always do absolute Value of modulo 2 to separate the scrolling into the 2 options through the modulo calculation allowing us to check the position of 0 or 1 to see in what scroll option we are in.  

Example position -16 would mean we are printing PID state because 16% = 0 and the first option is  PID state. 

#### Actions 

# CAD
We chose to use a simple CAD design that was simply a box to discretely hold all of our components. It featured a wheel on the top that was friction fit onto the shaft of a DC motor. We had to cut three different wheels because they were breaking when they made contact with a foriegn object. We had originally wanted to just use a long rectangle as our spinner but this was too hard to make accurate with the small size of the gap that it needed to fit through. We had some minor issues with the battery mount. We found that we were often swapping the batteries which was annoying to do because we had to remove our breadboard to access the pack. We solved this so we recut the bottom plate so that we could mount the battery pack facing out the bottom.


## OnShape Document
https://cvilleschools.onshape.com/documents/3df77543b07a8980f6919976/w/54537fa3957762533301028c/e/ac194388e2972accfd85d1c0





