import os
import numpy as np
from automobile import *
from environment import *
from agent import *
import matplotlib.pyplot as plt

"""
@TODO:
"""

def main():
	"""
		Sarsa is run from here and other hyper parameter optimizations can be done here. 
		actions: [0,1] -> [move, brake]
	"""

	num_iters           = 10
	num_episodes        = 2000
	time_steps          = 200
	
	max_negative_reward = -1000
	actions             = [ 0, 1 ]
	num_agents          = 2
	threshold			= 2
	discount_factor     = 1
	
	results = np.zeros((num_episodes))

	for i in range(num_iters):
		print "Iteration Number is:   ",i
		result = sarsa( num_episodes, time_steps, max_negative_reward, actions, discount_factor, num_agents, threshold)
		results += result


	# print result
	results = results/float(num_iters)
	episodes = range(num_episodes)

	plt.figure(1)
	plt.scatter(episodes, results)
	plt.ylim(-100,5)
	plt.xlim(0,num_episodes)
	plt.show()

	plt.figure(2)
	plt.scatter(episodes, results)
	plt.show()


def sarsa( num_episodes, time_steps, max_negative_reward, actions, discount_factor, num_agents , threshold):

	"""
	1. actions: 
			0 -> Do not warn the driver
			1 -> Warn the driver
	2. no_features:
		Around 40
	"""
	# Correct
	## Changing this parameter: The number of agents considered are 5. 
	## Only the nearest 5 agents are considered for feature extraction. 

	no_features  = num_agents*4*len(actions)

	returns_episodes = []
	weights = np.zeros(( no_features ))
	epsilon = 0.8

	# Correct
	for i in range(num_episodes):

		if(i%100==0):
			print ( "episode: ",i)	



		car    =  Automobile ( -100, 0, 1, 0)
		env    =  environment( num_agents )
		agents = env.get_agents()


		if(i%100==0):
			epsilon = epsilon/2

		agent_warning = warning( weights, no_features, num_agents,  car, env, epsilon )

		agent_reward = 0

		terminate = False
		count = 0

		while( not terminate and agent_reward > max_negative_reward and count < time_steps ):

			# print "Count: ",count
			count += 1
			"""
			Can update the feature vector here for the warning agent. 
			"""
			# This step is done. 
			env.take_one_step()

			agents_list = env.get_agents()

			# 2. 
			car_action  = car.get_action( threshold , agents_list )
			## Till here everything is correct. The environment is working perfectly. 

			if( car_action == 1 ):
				terminate = True

			if( not car.goal):
				car.action(car_action)
				agent_Rew     = agent_warning.update()
				agent_reward += agent_Rew
			else:
				break

			points = []
			points.append( [car.posX, car.posY])

			for i in range(len(agents)):
				points.append([agents[i].posX, agents[i].posY])

			points = np.array(points)

			# plt.scatter(points[ 0, 0],points[ 0, 1], color='green', linewidths = 3)
			# plt.scatter(points[ 1:, 0], points[ 1:, 1], color = 'blue', linewidths = 3)
			# plt.title("Environment. Green - Car with the warning agent, Blue - Other agents(Cars)")
			# plt.xlim( -100, 100)
			# plt.ylim( -100, 100)
			# plt.show()


		returns_episodes.append(agent_reward)
		weights = agent_warning.weights

		all_actions = agent_warning.all_actions

		# print "Number of 0's: ",all_actions.count(0)
		# print "Number of 1's: ",all_actions.count(1)
		# plt.hist(all_actions)
		# plt.ylim(0,200)
		# plt.show()

	return returns_episodes

if(__name__=='__main__'):
	main()