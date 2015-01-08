import os
from matplotlib import pyplot
import networkx as nx
from ComplexNetworkSim import *

### CONSTANTS ###
# States in the SIR model
SUSCEPTIBLE = 0
INFECTED = 1
RECOVERED = 2

# Simulation constants
MAX_SIMULATION_TIME = 100
TRIALS = 1

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
		self.infection_probability = 0.06 # 5% chance
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

	# visualiser = MyAnimationCreator(directory, myName, title, mapping, trial=trialToVisualise)
	# #gif speed can be changed by giving a parameter 'delay' (default=100) to AnimationCreator
	# visualiser.create_gif(verbose=True)

	temporary_export_to_gexf_fun("test", "SIR", "output.gexf")

def temporary_export_to_gexf_fun(path, name, output, trial=0):
	states, topos, vector = utils.retrieveTrial(path, trial)
 
	init_topo = topos[0][1]
	if topos[0][0] != 0:
		print "problem - first topology not starting at 0!"
	graph = init_topo
	nodes_states = [[] for n in graph.nodes()]

	i = 1 
	j = 0

	for t, s in states:
		# start with initial topology, and check the topology tuples
		# each time to make sure to have an up-to-date graph topology
		if len(topos) > i and t == topos[i][0]:								
			graph = topos[i][1]
			i += 1
		j += 1

		for node in range(len(s)):
			if len(nodes_states[node]) is 0 or nodes_states[node][-1][1] is not s[node]:
				nodes_states[node].append((t, s[node]))

	output_file = open(output, "w+")
	output_file.write(
		"""<?xml version="1.0" encoding="UTF-8"?>
		<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">
				<graph mode="dynamic" defaultedgetype="undirected" timeformat="integer">
						<attributes class="node" mode="dynamic">
								<attribute id="0" title="color" type="integer"/>
						</attributes>
						<nodes>
		""")

	# TODO: zijn nodes net zo gesorteerd als edges.
	for node in range(len(nodes_states)):
		output_file.write('<node id="{0}" label="{0}"><attvalues>'.format(node))
		for state in range(len(nodes_states[node])):
			if nodes_states[node][state][1] is SUSCEPTIBLE:
				state_str = '0'
			elif nodes_states[node][state][1] is INFECTED:
				state_str = '1'
			else:
				state_str = '2'

			start = nodes_states[node][state][0]

			# Last state
			if state is len(nodes_states[node]) - 1:
				output_file.write('<attvalue for="0" value="{}" start="{}"/>'.format(state_str, start))
			else:
				end = nodes_states[node][state + 1][0]

				output_file.write('<attvalue for="0" value="{}" start="{}" end="{}"/>'.format(state_str, start, end))
		output_file.write('</attvalues></node>')

	output_file.write("</nodes><edges>")

	edges = graph.edges()
	for edge_number, (edge_s, edge_t) in enumerate(edges):
		output_file.write('<edge id="{}" source="{}" target="{}" start="0"/>'.format(edge_number, edge_s, edge_t))

	output_file.write("</edges></graph></gexf>")
	output_file.close()

class MyAnimationCreator(object):
	def __init__(self, dir, name, title, mapping, trial=0, delay=100):
		self.name = name
		self.dir = os.path.abspath(dir)
		self.delay = delay
		self.mapping = mapping
		self.trial = trial
		self.title = title
		self.G = nx.Graph()
		
	def create_gif(self, verbose=True):
		self.createPNGs()

	def createPNGs(self):				
		states, topos, vector = utils.retrieveTrial(self.dir, self.trial)
								 
		init_topo = topos[0][1]
		if topos[0][0] != 0:
			print "problem - first topology not starting at 0!"
		self.G = init_topo
		self.layout = nx.layout.fruchterman_reingold_layout(self.G)
		self.nodesToDraw = self.G.nodes()
		self.edgesToDraw = self.G.edges()
		self.nodesToDraw.sort()
		self.edgesToDraw.sort()
		i = 1 
		j = 0

		pyplot.figure()
		for t, s in states:
			# start with initial topology, and check the topology tuples
			# each time to make sure to have an up-to-date graph topology
			if len(topos) > i and t == topos[i][0]:								
				self.G = topos[i][1]
				i += 1
			j += 1
			nx.write_gexf(self.G, "test2/" + self.name + "%02d.gexf" % j)