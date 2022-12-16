if __name__ == '__main__':
	import sys
	sys.path.insert(0, "../")

from PhysObjects.Particle import Particle
from PhysObjects.Wall import Wall
from Engine.Interactions import Interactions

from Engine.Settings import Settings as SETT
from MathUtilities.Vector import Vec2, Rotation2
from math import pi, atan

class CollisionDetection:
	def __init__(self):
		self.bSetWallCollision = True

	def setWallCollision(self, activate=True):
		self.bSetWallCollision = activate

	def detectCollision(self, particle, phyObject):
		x = particle.pos[0]
		y = particle.pos[1]

		# calculate the distance of collision by straight trajectory 
		distance = phyObject.calculateDistanceTo(particle.pos)
		if (type(phyObject)==Wall) and (distance < particle.radius):
			return True
		elif (type(phyObject)==Particle) and (distance < phyObject.radius + particle.radius):
			return True
		else: 
			return False

	def getTimeOfImpact(self, particle, phyObject):
		x1 = particle.pos[0]
		y1 = particle.pos[1]
		x0 = particle.prev_pos[0]
		y0 = particle.prev_pos[1]
		slope = (y1 - y0)/(x1 - x0) if x0!=x1 else 'inf'			
		trajectory_vector = Vec2(x1-x0, y1-y0)
		
		# calculate angle of trajectory relative to the x-axis
		angle = pi/2
		if x0 != x1:
			angle = atan(trajectory_vector[1]/trajectory_vector[0])
			if angle < 0:
				angle += pi

		phyObject.getRelTangent(particle)


if __name__ == '__main__':
	colDetect = CollisionDetection()
	particle = Particle(
		init_pos=[SETT.WIN_WIDTH/2, SETT.WIN_HEIGHT/2],
		init_vel=[0, 1],
		)
	sides = ['up', 'down', 'right', 'left']
	walls = [Wall(side=side) for side in sides]
	

	while True:
		print(particle)
		particle.move()
		for wall in walls:
			collision = colDetect.detectCollision(particle, wall)
			if collision:
				print("puk")
			print(particle)
				


