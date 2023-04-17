A small library to display live output on a line graph

## Installation 
you can download the file and place it in the root of your script folder

## Get started 
how to create and output the graph while controlling the graph with the 
tkinter scale widget to simulate input or pass your own input value

```python
from plotLive import liveGraph

graph = liveGraph(Ylimits=[0,20],TkinterScale=True)
# limits of the graph set in list and tkinter widget activated 

while True:
    graph.update()
```

