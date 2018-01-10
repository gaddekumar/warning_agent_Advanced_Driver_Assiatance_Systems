import os
import numpy as np
from automobile import *


## Restrict the environment. This has to be done in the automobile class only. 
class environment(object):

	def __init__(self, num, start_x = None, start_y=None):


		self.number_of_agents = num
		self.avoid_x = start_x
		self.avoid_y = start_y
		self.agents = []

		
		for i in range(self.number_of_agents):
			## Create all the agents here. 
			x = np.random.randint( -100, 100)
			y = np.random.randint( -100, 100)

			vel_x = np.random.randint(-5, 5)
			vel_y = np.random.randint(-5, 5)

			while(vel_x==0 and vel_y ==0):
				vel_x = np.random.randint(-5, 5)
				vel_y = np.random.randint(-5, 5)

			agent = Automobile( x, y, vel_x, vel_y, time_step = 1)
			self.agents.append(agent)


	def take_one_step(self):
		"""
		Take all the agents and move one step ahead. 
		"""
		for i in range(len(self.agents)):
			self.agents[i].action(0)

	def get_agents(self):
		return self.agents

		
if(__name__=='__main__'):
	main()