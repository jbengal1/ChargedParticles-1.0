import sys
from Geometry.Circle import Circle
from Engine.Interactions import GRAVITY

if __name__=='__main__':
	# Add Engine directory to path
	sys.path.insert(0, "../")

	# Add main directory to path
	sys.path.insert(0, "../../")

from MathUtilities.Vector import Vec2
from Engine.Settings import Settings as SETT

class Particle(Circle):
	def __init__(self, 
		init_pos=[0, 0], init_vel=[0, 1],
		radius=10,
		electricCharge = -1,
		index = None
		):
		self.radius = self.mass = radius
		self.electricCharge = electricCharge
		self.index = None if index is None else int(index)

		self.pos = Vec2(init_pos[0], init_pos[1])
		self.vel = Vec2(init_vel[0], init_vel[1])
		self.accel = Vec2(0, 0)
		
		# This is the force vector applied on the particle.
		# After interaction it's calculated with newton second law
		self.netForce = Vec2(0, 0)
		self.arrForces = []
		self.collisionForces = []

		self.momentum = self.mass*self.vel
		self.prev_momentum = self.mass*self.vel
		self.kinetic_energy = 0.5*self.mass*self.vel*self.vel
		self.gravity_energy = -self.mass*GRAVITY*self.pos[1] 
		self.potential_energy = sum([
			self.gravity_energy
			])
		self.total_energy = self.kinetic_energy + self.potential_energy
		self.prev_pos = self.pos
		
		self.atRest = [False, False]

		# Range between 0 and 1. 
		# where 1 is total elastic (full energy conservation)
		# and 0 is not elastic (all energy being deposit)
		self.elasticity = 1

	def __str__(self):
		str_pos = f'pos:\t{self.pos()}\n'
		str_vel = f'vel:\t{self.vel()}\n'
		str_accel = f'accel:\t{self.accel()}\n'
		str_force = f'applied force:\t{self.netForce()}\n'
		str_mom = f'momentum:\t{self.momentum()}\n'
		return str_pos + str_vel + str_accel + str_force + str_mom + '\n'

	def recordPrevious(self)->None:
		# First I save the previous state for later use.
		self.prev_pos = self.pos
		self.prev_vel = self.vel
		self.prev_accel = self.accel
		self.prev_momentum = self.momentum

	def moveFree(self, method_name='')->None:
		''' calculate every kinematic variable using euler's method '''

		# Save the current state before changing all values
		self.recordPrevious()

		# Update values by chosen method.
		# If none is given, default is euler
		if method_name in ['', 'euler', 'Euler', 'Eu']:
			self.EulerMethod()
		if method_name in ['verlet', 'ver']:
			self.VerletMethod()

		# Update energies and all kinematics dictionary 
		self.updateAccel()
		self.updateMomentum()
		self.updateEnergies()
		# self.updateDictionary()
	
	def EulerMethod(self)->None:
		""" Updates the position and velocity of by Euler's method

		This method updates the position and velocity of the particle according to Euler's method, solving first-order ODE.
		"""
		self.pos = self.pos + self.vel*SETT.DT + 0.5*self.accel*SETT.DT**2
		self.vel = self.vel + self.accel*SETT.DT

	def VerletMethod(self)->None:
		""" Updates the position and velocity of by Verlet integration

		This method updates the position and velocity of the particle according to Verlet integration, solving second-order ODE.
		"""
		self.pos = self.pos + self.vel*SETT.DT + 0.5*self.accel*SETT.DT**2
		self.vel = self.vel + 0.5* (self.accel + self.netForce/self.mass) *SETT.DT

	def moveByMomentum(self)->None:
		""" calculates and updates every kinematic variable by the current momentum.

		This method calculates and updates every kinematic variable by the current momentum.
		This update is intended to be applied after calculating the change in momentum, which is after a collision.
		"""

		# Save the current state before changing all values
		self.recordPrevious()

		# Update values
		self.accel = self.netForce/self.mass
		self.vel = self.momentum/self.mass 
		self.pos = self.pos + self.vel*SETT.DT
		self.updateEnergies()
		# self.updateDictionary()

	def stepBack(self)->None:
		"""Updates each kinematic attribute back to it's previous time step value.
		"""
		self.pos = self.prev_pos
		self.vel = self.prev_vel
		self.accel = self.prev_accel
		self.momentum = self.prev_momentum
		self.updateEnergies()

	def setVel(self, velocity=list)->None:
		if velocity==[] or velocity==list:
			print("Velocity list is empty or None is given.")
			return None
		try:
			self.vel = Vec2(velocity[0], velocity[1])
		except BaseException:
			print(f"Can't convert {type(velocity)} to Vec2.")

	def setForce(self, force=list)->None:
		try:
			if type(force)==list:
				self.netForce = Vec2(force[0], force[1])
			elif type(force)==Vec2:
				self.netForce = force
		except BaseException:
			print(f"Can't convert {type(force)} to Vec2.")

	def applyForce(self, force=list, fromCollision=False)->None:
		try:
			if type(force)==list:
				self.arrForces.append(Vec2(force[0], force[1]))
				if fromCollision:
					self.collisionForces.append(Vec2(force[0], force[1]))
				self.updateNetForce(force)
			elif type(force)==Vec2:
				self.arrForces.append(force)
				if fromCollision:
					self.collisionForces.append(force)
				self.updateNetForce(force)
			else:
			 	raise Exception(f"Can't convert {type(force)} to Vec2.")
		
		except BaseException:
			print(f"Can't convert {type(force)} to Vec2.")
	
	def updateAccel(self):
		self.accel = self.netForce/self.mass
	
	def updateMomentum(self):
		self.momentum = self.mass*self.vel
	
	def updateNetForce(self, force):
		self.netForce += force

	def updateEnergies(self):
		self.kinetic_energy = 0.5*self.mass*self.vel*self.vel
		self.gravity_energy = -self.mass*GRAVITY*self.pos[1] 
		self.potential_energy = sum([
			self.gravity_energy
			])
		self.total_energy = self.kinetic_energy + self.potential_energy

	# def calculateNetForce(self):
	# 	for force in self.arrForces:
	# 		self.netForce += force

	def resetForces(self):
		self.netForce = Vec2(0, 0)
		self.arrForces = []
		self.collisionForces = []

	# def getAttribute(self, key):
	# 	return self.dictionary[key]


if __name__ == '__main__':
	particle = Particle(
		init_pos=[SETT.WIN_WIDTH/2, SETT.WIN_HEIGHT/2],
		init_vel=[1, 0],
		)

	print(particle)
	particle.move()
	print(particle)
	particle.move()
	print(particle)