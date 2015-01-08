import networkx as nx
from ComplexNetworkSim import *

### CONSTANTS ###
# States in the SIR model
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# Simulation constants
MAX_SIMULATION_TIME = 25.0
TRIALS = 2

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
	simulation = NetworkSimulation(graph,
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

def plotSim():
	directory = 'test' #location of simulation result files
	myName = "SIR" #name that you wish to give your image output files
	title = "Simulation of agent-based simple SIR"
	#define three simulation-specific constants:
	SUSCEPTIBLE = 0
	INFECTED = 1
	RECOVERED = 2

	statesToMonitor = [INFECTED, SUSCEPTIBLE] #even if we have states 0,1,2,3,... plot only 1 and 0
	colours = ["r", "g"] #state 1 in red, state 0 in green
	labels = ["Infected", "Susceptible"] #state 1 named 'Infected', 0 named 'Susceptible'

	mapping = {SUSCEPTIBLE:"w", INFECTED:"r", RECOVERED:"0.4"}
	trialToVisualise = 0

	p = PlotCreator(directory, myName, title, statesToMonitor, colours, labels)
	p.plotSimulation(show=True)
	#show=True shows the graph directly,
	#otherwise only a png file is created in the directory defined above.

	visualiser = AnimationCreator(directory, myName, title, mapping, trial=trialToVisualise)
	#gif speed can be changed by giving a parameter 'delay' (default=100) to AnimationCreator
	visualiser.create_gif(verbose=True)