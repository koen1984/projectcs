import matplotlib.pyplot as plt
import networkx as nx

def plot(graph):
	nx.draw(graph)
	plt.show()

def export_GEXF(graph, path):
	nx.write_gexf(graph, path)
