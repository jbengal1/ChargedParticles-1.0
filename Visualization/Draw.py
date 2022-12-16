import pygame
# from pygame.locals import DOUBLEBUF
if __name__ == '__main__':
	import sys
	sys.path.insert(0, "../")
from Engine.Settings import Settings as SETT
from Visualization.Colors import *
from PhysObjects.Particle import Particle
from PhysObjects.Wall import Wall

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pylab

matplotlib.use("Agg")
plt.rcParams.update({'figure.max_open_warning': 0})

class DrawManager:
	def __init__(self):
		self.window = pygame.display.set_mode((SETT.WIN_WIDTH, SETT.WIN_HEIGHT))
		self.screen1 = pygame.Surface((SETT.SCREEN1_WIDTH, SETT.SCREEN1_HEIGHT))
		self.screen2 = pygame.Surface((SETT.SCREEN2_WIDTH, SETT.SCREEN2_HEIGHT))
		pygame.display.set_caption("charged particles simulation")
		# self.clock = pygame.time.Clock()
		self.screen1.fill('black')
		self.screen2.fill('black')

	def drawAll(self, shapes):
		self.screen1.fill('black')
		for shape in shapes:
			self.drawShape(shape)

	def drawShape(self, shape):
		if type(shape) == Wall:
			pygame.draw.line(self.screen1, WHITE , shape.p1, shape.p2, shape.thickness)
		if type(shape) == Particle:
			pygame.draw.circle(self.screen1, WHITE, shape.pos, shape.radius)

	def drawText(self, text=None):
		if text is not None:
			text.draw(self.screen1)

	def update(self):
		self.window.blit(self.screen1, (0, 0))
		self.window.blit(self.screen2, (0, SETT.SCREEN1_HEIGHT))
		pygame.display.update()
		# self.clock.tick(FPS)

	def plot2D(self, x, recorders, x_axis="", y_axis="", title="", logY=False):
		self.screen2.fill('black')
		fig = pylab.figure(
			figsize=[18, 2.5], # Inches
	        dpi=100        # 100 dots per inch
	        )
		ax = fig.gca()

		for recorder in recorders:
			ax.plot(x, recorder.record_arr)
		ax.set_title(title)
		canvas = agg.FigureCanvasAgg(fig)
		canvas.draw()
		renderer = canvas.get_renderer()
		raw_data = renderer.tostring_rgb()

		size = canvas.get_width_height()

		surf = pygame.image.fromstring(raw_data, size, "RGB")
		self.screen2.blit(surf, (0, 0))