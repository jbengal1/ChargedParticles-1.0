import sys

if __name__=='__main__':
	# Add Engine directory to path
	sys.path.insert(0, "../")

	# Add main directory to path
	sys.path.insert(0, "../../")

from Engine.Settings import *
from MathUtilities.Vector import Vec2
from Geometry.Line import Line

class Wall(Line):
	def __init__(self, 
		p1=[0,0], p2=[10,10],
		side=None
		):
		super(Wall, self).__init__(p1, p2, name=f"wall {side}")
		self.p1 = p1
		self.p2 = p2
		self.side = side
		
		self.mass = 'inf'
		self.vel = Vec2(0, 0)
		self.pos = Vec2(p1[0] + p2[0], p1[1] + p2[1])/2

	def __str__(self):
		if self.name is not None:
			return self.name
		return 'wall default'


if __name__ == '__main__':
	sides = ['up', 'right', 'down', 'left']
	walls_coordinates = [
		[ [0, 0], [WIN_WIDTH, 0] ],
		[ [WIN_WIDTH, 0], [WIN_WIDTH, WIN_HEIGHT] ],
		[ [WIN_WIDTH, WIN_HEIGHT], [0, WIN_HEIGHT] ],
		[ [0, WIN_HEIGHT], [0, 0] ],
	]
	walls = []
	for walls_coordinates, side in zip(walls_coordinates, sides):
		walls.append( Wall(walls_coordinates[0], walls_coordinates[1], side=side) )
	for wall in walls:
		print(wall, wall.slope, wall.y_intersection)
