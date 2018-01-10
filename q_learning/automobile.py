import os
import numpy as np



class Automobile(object):


	def __init__(self, initial_x, initial_y, vel_x, vel_y, time_step=1):
		"""
		1. Start position of the car
		2. End position of the car
		3. Starting velocity of the car. 
		4. Consider the velocity of the car is constant.
		"""

		self.posX = initial_x
		self.posY = initial_y
		self.velocityX = vel_x
		self.velocityY = vel_y

		self.time_step = time_step
		self.left_bound = -100
		self.right_bound = 100
		self.top_bound = 100
		self.bottom_bound = -100
		self.braked = 0
		self.goal = False

		self.nextX = initial_x
		self.nextY = initial_y


	def distance(self, pt1, pt2):
		return np.sqrt((pt2[0]-pt1[0])**2 + (pt2[1]-pt1[1])**2)


	def action(self, action):
		"""
		There are multiple actions here. One is to move right or left and the other action is to brake the car. 
		Inputs: 
			1. action: (str)
				1. brake
				2. move_right
				3. Can be extended for complex models.
		returns: 
			1. Next position of the car. 
			2. 
			3. 
		"""
		self.posX = self.nextX
		self.posY = self.nextY

		if(action == 1):
			self.braked = 1
			return (self.posX, self.posY)

		elif(action == 0):
			self.braked = 0

			## X update
			self.nextX  += self.velocityX*self.time_step
			if(self.nextX>self.right_bound):
				self.nextX = self.right_bound
				self.velocityX = np.random.randint(-5,5)
			if(self.nextX < self.left_bound):
				self.nextX = self.left_bound
				self.velocityX = np.random.randint(-5,5)
				
			## Y update
			self.nextY  += self.velocityY*self.time_step
			if(self.nextY > self.top_bound):
				self.nextY = self.top_bound
				self.velocityY = np.random.randint(-5, 5)
			if(self.nextY< self.bottom_bound):
				self.nextY = self.bottom_bound
				self.velocityY = np.random.randint(-5, 5)

			return (self.nextX, self.nextY)

	def get_action(self, threshold, agents):
		"""
		This method encodes the actual behavior of the perfect driver. When the distance between the vehicle 
		and the other agents is less than certain threshold, then the driver stops. 
		"""

		min_value = 200*200
		for i in range(len(agents)):
			pr_agent = agents[i]
			pos_pr_agent = pr_agent.getPosition()
			d = self.distance( pos_pr_agent, (self.posX, self.posY))
			if (d<min_value):
				min_value = d

		self.goal = False

		if(self.posX >= self.right_bound or self.posY>=self.top_bound):
			self.goal = True

		if (min_value<=threshold):
			return 1
		else:
			return 0
	
		
	def goal_reached(self):
		return self.goal

	def getPosition(self):
		return (self.posX, self.posY)

	def getStatus(self):
		return self.braked
