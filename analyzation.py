import networkx as nx
import matplotlib.pyplot as plt

def diameter(graph):
  return nx.diameter(graph)

def clustering_coefficient(graph):
  print("to do: clustering_coefficient")

def degree_distribution(graph):
  graph = nx.fast_gnp_random_graph(10, 0.2)
  degree_sequence=sorted(nx.degree(graph).values(),reverse=True) # degree sequence
  #print "Degree sequence", degree_sequence
  dmax=max(degree_sequence)

  plt.loglog(degree_sequence,'b-',marker='o')
  plt.title("Degree rank plot")
  plt.ylabel("degree")
  plt.xlabel("rank")

  # draw graph in inset
  plt.axes([0.45,0.45,0.45,0.45])
  Gcc=sorted(nx.connected_component_subgraphs(graph), key = len, reverse=True)[0]
  pos=nx.spring_layout(Gcc)
  plt.axis('off')
  nx.draw_networkx_nodes(Gcc,pos,node_size=20)
  nx.draw_networkx_edges(Gcc,pos,alpha=0.4)

  plt.savefig("degree_histogram.png")
  plt.show()