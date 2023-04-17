from plotLive import liveGraph

graph = liveGraph(Ylimits=[0,20],TkinterScale=True)

while True:
    graph.update()