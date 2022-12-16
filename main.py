from Engine.Settings import *
from Simulations import Simulation1

if VISUAL_ON:
	import pygame
	pygame.init()

class App:
	def __init__(self):
		self.simulations = [Simulation1()]

	def run(self):
		self.simulations[0].run()

	
if __name__ == '__main__':
	app = App()
	app.run()