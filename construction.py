import networkx as nx

def construct_erdos_reyni(n, p):
	return nx.fast_gnp_random_graph(n, p)

def construct_watts_strogatz(n, k, p):
	return nx.watts_strogatz_graph(n, k, p)


def construct_barabasi_albert(n, m):
	return nx.barabasi_albert_graph(n, m)
