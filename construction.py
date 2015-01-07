import networkx as nx

def construct_erdos_reyni(n, p):
	print("to do: construct_erdos_reyni")
	return nx.fast_gnp_random_graph(n, p)

def construct_watts_strogatz(n, k, p):
	print("to do: construct_watts_strogatz")
	return nx.watts_strogatz_graph(n, k, p)


def construct_barabasi_albert(n, m):
	print("to do: construct_barabasi_albert")
	return nx.barabasi_albert_graph(n, m)
