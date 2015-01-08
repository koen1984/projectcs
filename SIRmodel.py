import networkx as nx
from ComplexNetworkSim import NetworkAgent, Sim

### CONSTANTS ###
# States in the SIR model
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

def simulate(graph):
	# Initualize all nodes as susceptible
	states = [SUSCEPTIBLE for n in graph.nodes()]
	# Infect 1 node
	states[0] = INFECTED
	directory = 'test' #output directory

	# run simulation with parameters
	# - complex network structure
	# - initial state list
	# - agent behaviour class
	# - output directory
	# - maximum simulation time
	# - number of trials
	simulation = NetworkSimulation(G,
																 states,
																 SIRSimple,
																 directory,
																 MAX_SIMULATION_TIME,
																 TRIALS)
	simulation.runSimulation()

class SIRSimple(NetworkAgent):
	""" an implementation of an agent following the simple SIR model """

	def __init__(self, state, initialiser):
		NetworkAgent.__init__(self, state, initialiser)
		self.infection_probability = 0.05 # 5% chance
		self.infection_end = 5

	def Run(self):
		while True:
			if self.state == SUSCEPTIBLE:
				self.maybeBecomeInfected()
				yield Sim.hold, self, NetworkAgent.TIMESTEP_DEFAULT #wait a step
			elif self.state == INFECTED:
				yield Sim.hold, self, self.infection_end	#wait end of infection
				self.state = RECOVERED
				yield Sim.passivate, self #remove agent from event queue

	def maybeBecomeInfected(self):
		infected_neighbours = self.getNeighbouringAgentsIter(state=INFECTED)
		for neighbour in infected_neighbours:
			if SIRSimple.r.random() < self.infection_probability:
				self.state = INFECTED
				break