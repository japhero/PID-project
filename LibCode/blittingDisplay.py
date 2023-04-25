from plotLive import liveGraph
import math

graph = liveGraph(Ylimits=[0,20],InputItems=[0,1])

for x in range(1000):
    graph.update(Input=[3,4])

