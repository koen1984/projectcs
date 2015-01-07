from construction import *
from analyzation import *
from visualization import *

if __name__ == '__main__':
	graph = None

	# Hardcoded commands for debugging
	debug_commands = [
		"construct 1",
		"diameter",
		"plot"
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
			parameter_error = False
			if len(user_input) is not 2:
				parameter_error = True

			elif user_input[1] == "1":
				graph = construct_erdos_reyni(100, 0.01)
				plot(graph)
			elif user_input[1] == "2":
				graph = construct_watts_strogatz(100, 3, 0.01)
				plot(graph)
			elif user_input[1] == "3":
				graph = construct_barabasi_albert(100, 5)
				plot(graph)
			else:
				parameter_error = True

			if parameter_error:
				print("Invalid parameters")
				print("Correct use: construct [network type]")
				print("(network types: 1 = Erdos-Reyni, 2 = Watts-Strogatz, 3 = Barabasi-Albert)")

		elif user_input[0] == "diameter":
			diameter(graph)

		elif user_input[0] == "clustering":
			clustering_coefficient(graph)

		elif user_input[0] == "degree":
			degree_distribution(graph)

		elif user_input[0] == "plot":
			plot(graph)

		else:
			print("Unknown command. Accepted commands:")
			print("construct [network type]")
			print("diameter")
			print("clustering")
			print("degree")
			print("plot")

		print()
