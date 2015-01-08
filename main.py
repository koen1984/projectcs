from construction import *
from analyzation import *
from SIRmodel import *
from visualization import *

if __name__ == '__main__':
	graph = None

	# Hardcoded commands for debugging
	debug_commands = [
		"construct 1",
	]

	while True:
		if len(debug_commands) is 0:
			user_input = raw_input("> ").split()
		else:
			user_input = debug_commands[0].split()
			del(debug_commands[0])

		# Stop program
		if len(user_input) is 0:
			break

		# Construct graph
		elif user_input[0] == "construct":
			error = False
			if len(user_input) is 1:
				print "Invalid parameters"
				print "Correct use: construct [network type]"
				print "(network types: 1 = Erdos-Reyni, 2 = Watts-Strogatz, 3 = Barabasi-Albert)"
				error = True

			elif user_input[1] == "1":
				if len(user_input) is not 4:
					nNodes = 100
					prob = 0.1
				else:
					nNodes = int(user_input[2])
					prob = float(user_input[3])
				graph = construct_erdos_reyni(nNodes, prob)

			elif user_input[1] == "2":
				if len(user_input) is not 5:
					nNodes = 100
					nNeighbours = 4
					prob = 0.1
				else:
					nNodes = int(user_input[2])
					nNeighbours = int(user_input[3])
					prob = float(user_input[4])
				graph = construct_watts_strogatz(nNodes, nNeighbours, prob)

			elif user_input[1] == "3":
				if len(user_input) is not 4:
					nNodes = 100
					nNeighbours = 4
				else:
					nNodes = int(user_input[2])
					nNeighbours = int(user_input[3])
				graph = construct_barabasi_albert(nNodes, nNeighbours)

			else:
				error = True

			if not error and graph is not None:
				plot(graph)

		elif user_input[0] == "diameter":
			diameter(graph)

		elif user_input[0] == "clustering":
			clustering_coefficient(graph)

		elif user_input[0] == "degree":
			degree_distribution(graph)

		elif user_input[0] == "plot":
			plot(graph)

		elif user_input[0] == "simulate":
			simulate(graph)

		elif user_input[0] == "plotSim":
			plotSim()

		elif user_input[0] == "export":
			path = "output.gexf"
			if len(user_input) is 2:
				path = user_input[1]
			export_GEXF(graph, path)

		else:
			print "Unknown command. Accepted commands:"
			print "construct [network type]"
			print "diameter"
			print "clustering"
			print "degree"
			print "plot"

		print ""
