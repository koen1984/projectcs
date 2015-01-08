import matplotlib.pyplot as plt
import networkx as nx

def plot(graph):
	nx.draw(graph)
	plt.show()

def export_GEXF(graph, path):
	if graph is None:
		print "Error: no graph to export"
	elif path is None or path == "":
		print "Error: no path to export to"
	else:
		nx.write_gexf(graph, path)
		print "Exported to " + path
