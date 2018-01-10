import os
import random
import numpy as np
from automobile import *
from environment import *

"""
TODO's: 
1. This part is done. Do normalization in the feature_vector
"""

class warning(object):

	def __init__( self, weights, num_features, num_agents, car_object, env, epsilon, learning_rate = 1e-3):
		
		self.epsilon = epsilon
		self.weights = weights
		self.car     = car_object
		self.env     = env
		self.discount_factor = 1

		### Model Variables
		self.next_q_value           = 0
		self.pres_q_value           = 0
		self.learning_rate          = learning_rate
		self.present_feature_vector = np.zeros((num_features))
		self.next_feature_vector    = np.zeros((num_features))
		self.num_features           = num_features
		self.cross_check            = 0
		self.reward                 = 0
		self.num_agents             = num_agents
		self.all_actions            = []


	def update(self):

		pres_action = self.get_action("present", self.epsilon)
		agent_reward = self.get_reward( pres_action, self.car.braked)
		
		next_action = self.get_action("next", 0)
		self.all_actions.append( pres_action )

		td_error = agent_reward + self.discount_factor*self.next_q_value - self.pres_q_value
		update   = self.learning_rate*td_error*self.present_feature_vector

		self.weights  += update

		# self.pres_q_value = self.next_q_value
		# self.present_feature_vector = self.next_feature_vector

		return agent_reward
		

	def get_action(self, time_step, epsilon):

		actions = [ 0, 1]

		array2 = []
		array3 = []

		for i in actions:
			features_obtained = self.getFeatureVector(i, time_step)
			q_value = np.sum( self.weights*features_obtained )

			array2.append( q_value )
			array3.append( features_obtained )
			

		max_index = array2.index(max(array2))
		a_prime = self.epsilon_greedy_action( max_index, epsilon)

		# print a_primes
		if(time_step=="present"):
			self.pres_q_value = array2[a_prime]
			self.pres_feature_vector = array3[a_prime]

		elif(time_step == "next"):
			self.next_q_value = array2[a_prime]
			self.next_feature_vector = array3[a_prime]
		return a_prime


	def get_reward( self, a_prime, car_is_braked):

		if  (a_prime == 0 and car_is_braked == 0):
			return 0

		elif(a_prime == 1 and car_is_braked == 0):
			return -1

		elif(a_prime == 0 and car_is_braked == 1):
			return -1

		elif(a_prime == 1 and car_is_braked == 1):
			return 1

		return -1

	def get_reward2( self, a_prime, car_is_braked):

		if( self.cross_check == 1 and car_is_braked ==0):
			return -1
		
		elif(a_prime == 1 and car_is_braked == 0 and self.cross_check == 0):
			self.cross_check = 1
			return -1

		elif( self.cross_check == 1 and car_is_braked==1):
			self.cross_check = 0
			return -1

		return 0

	def getFeatureVector( self, action, time_step):

		"""
		car_state : State of the car. (x,y, Vx, Vy)
		agents: List of all the agents in the environment. 
		"""
		# print "Time step is: ",time_step

		if(time_step == "present"):
			pos_carX = self.car.posX
			pos_carY = self.car.posY
			vel_carX = self.car.velocityX
			vel_carY = self.car.velocityY

		else:
			pos_carX = self.car.nextX
			pos_carY = self.car.nextY
			vel_carX = self.car.velocityX
			vel_carY = self.car.velocityY

		## Feature vector is of the length - (2 * Number of features)
		## Return based on the action.

		## Need to change this part. 
		num_features = self.num_features

		final_feature_vector = np.zeros((num_features))

		feature_vector = []
		r_distances = []

		for i in range( len( self.env.agents ) ):

			a_posX = self.env.agents[i].posX
			a_posY = self.env.agents[i].posY
			a_velX = self.env.agents[i].velocityX
			a_velY = self.env.agents[i].velocityY

			r_posX = float(pos_carX - a_posX)/200.0
			r_posY = float(pos_carY - a_posY)/200.0
			r_velX = float(vel_carX - a_velX)/10.0
			r_velY = float(vel_carY - a_velY)/10.0

			# r_dist = np.sqrt(r_posX**2 + r_posY**2)
			# r_distances.append(r_dist)

			# feature_vector.append([r_posX, r_posY, r_velX, r_velY])
			feature_vector.append(abs(r_posX))
			feature_vector.append(abs(r_posY))
			feature_vector.append(r_velX)
			feature_vector.append(r_velY)

		final_feature_vector[ action*num_features/2:action*num_features/2+num_features/2] = feature_vector
		return final_feature_vector

	def epsilon_greedy_action(self, action, epsilon):

		random_number = np.random.random()
		actions = [ 0, 1]

		if(random_number > epsilon):
			return action
		else:
			return random.choice(actions)

