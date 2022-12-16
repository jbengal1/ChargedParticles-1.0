from math import *

if __name__ == '__main__':
	import sys
	sys.path.insert(0, "../")

from Engine.Settings import Settings as SETT
from MathUtilities.Vector import Vec2, Rotation2
from PhysObjects.Wall import Wall
from Geometry.Line import Line
GRAVITY = -1000 if SETT.GRAVITY_ON else 0

class Interactions:
	def __init__(self,
		gravity=GRAVITY,
		permittivity=1e10
		):
		if SETT.GRAVITY_ON:
			self.gravity = gravity
		else:
			self.gravity = 0

		if SETT.ELECTRICITY_ON:
			self.permittivity = permittivity
		else:
			self.permittivity = 0

	def applyGravity(self, particle)->None:
		g = Vec2(0, self.gravity)
		particle.applyForce(particle.mass*g)

	def applyNormalForce(self, collObject, applObject)->None:
		netForce = applObject.netForce
		norm = collObject.norm

		rel_angle = netForce.getTheta() - collObject.norm.getTheta()
		if rel_angle > 0:
			normalForce = Rotation2(netForce, -rel_angle)
		else:
			normalForce = Rotation2(netForce, rel_angle)
		
		applObject.applyForce(normalForce, fromCollision=True)


	def applyElectricForce(self, particle1, particle2)->None:
		# Get the particles relevant attributes
		r1, q1 = particle1.pos, particle1.electricCharge
		r2, q2 = particle2.pos, particle2.electricCharge
		relative_vector = r1 - r2

		# Calculate the relative force
		decreaseFactor = 0.001 
		electricForce = decreaseFactor*self.permittivity*q1*q2*(relative_vector/relative_vector.getNorm()**3)

		# Apply the force on each of the two particles
		particle1.applyForce(electricForce, fromCollision=False)
		particle2.applyForce(-electricForce, fromCollision=False)


	def FindTrajectory(self, wall, particle):
		''' Updates the new position according to CCD (Continuous Collision Detection)'''
		pass

	
	def updateMomentum(self, collObject, applObject):
		m1, m2 = collObject.mass, applObject.mass
		v1, v2 = collObject.vel, applObject.vel
		r1, r2 = collObject.pos, applObject.pos

		if type(collObject) == Wall:
			rel_angle = collObject.relAngleVec(r2)
			Rotation2(r1, rel_angle)
			if collObject.mass == 'inf':
				# v2 = v2 - 2*(r2-r1)*((v2-v1)*(r2-r1))/((r2-r1).getNorm())**2

				# if applObject.momentum.getNorm() > 1e-12:
				rel_angle = collObject.relAngleVec(applObject.momentum)
				if rel_angle >= 90:
					rotate_angle = -(180 - rel_angle)
				else:
					rotate_angle = rel_angle

				# This is the change in momentum. 
				# Conserved if elastic parameter is 1
				# applObject.momentum = Rotation2(applObject.momentum, 2*rotate_angle)*applObject.elasticity
				applObject.momentum = Rotation2(applObject.momentum, 2*rotate_angle)
				for i, p in enumerate(applObject.momentum):
					if abs(p) < 1e-12:
						applObject.momentum[i] = 0
						applObject.atRest[i] = True
			
		else:
			new_v1 = v1 - ((v1-v2)*(r1-r2))*(2*m2/(m1+m2))*(r1-r2)/((r1-r2).getNorm())**2
			new_v2 = v2 - ((v2-v1)*(r2-r1))*(2*m1/(m1+m2))*(r2-r1)/((r2-r1).getNorm())**2
			
			collObject.momentum = collObject.mass*new_v1
			applObject.momentum = applObject.mass*new_v2
			
	def findNeighbors(self, particle_index, particles, length):
		x1, y1 = particles[particle_index].pos[:]
		r1 = particles[particle_index].radius
		indices = []
		for i, particle in enumerate(particles):
			if i != particle_index:
				x2, y2 = particle.pos[:]
				r2 = particle.radius
				flag = abs(x1-x2) < r1 + r2 + length or abs(y1-y2) < r1 + r2 + length
				if flag:
					indices.append(i)
		
		return indices
			



    