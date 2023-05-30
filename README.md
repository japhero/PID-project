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

# CAD
We chose to use a simple CAD design that was simply a box to discretely hold all of our components. It featured a wheel on the top that was friction fit onto the shaft of a DC motor. We had to cut three different wheels because they were breaking when they made contact with a foriegn object. We had originally wanted to just use a long rectangle as our spinner but this was too hard to make accurate with the small size of the gap that it needed to fit through. We had some minor issues with the battery mount. We found that we were often swapping the batteries which was annoying to do because we had to remove our breadboard to access the pack. We solved this so we recut the bottom plate so that we could mount the battery pack facing out the bottom.


## OnShape Document
https://cvilleschools.onshape.com/documents/3df77543b07a8980f6919976/w/54537fa3957762533301028c/e/ac194388e2972accfd85d1c0





