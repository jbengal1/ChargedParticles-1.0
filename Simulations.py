import pygame
from pygame.locals import *
import json
import random

# PATHS
import sys, os
PATH_SOUNDS_DIR = "Sounds"

from Engine.Settings import Settings as SETT
from Engine.CollisionDetection import CollisionDetection
from PhysObjects.Particle import Particle
from PhysObjects.Wall import Wall
from Visualization.Draw import DrawManager
from Visualization.Text import Text, TimeText
from Visualization.Colors import *
from Engine.Interactions import Interactions


colDetect = CollisionDetection()
drawManager = DrawManager()
interactions = Interactions()
fpsText = Text(x=0, y=0, color=BRIGHT_BLUE, font_settings=('freesansbold.ttf', 18))
timeText = TimeText(time=0, x=0, y=40, color=BRIGHT_BLUE, font_settings=('freesansbold.ttf', 18))



class Recorder:
	def __init__(self, simulation=None):
		self.simulation = simulation
		self.activate_record = False
		self.record_attribute = ""
		self.record_arr = []

	def record(self, attribute: str, init_time: float, fin_time: float, activate=True)->None:
		self.record_attribute = attribute
		self.init_time = init_time
		self.fin_time = fin_time
		self.activate_record = activate


class Simulation1:
	def __init__(self, 
		state_fileName='initState-random.json',
		path_name='InitialStates', 
		state_name=None,
		init_time=0.0
		): 

		# self.display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()

		# Set initial particles states
		self.particles = []
		if state_name is None:
			import re
			state_name = re.split('-| |\.', state_fileName)[1]
		self.loadState(
			file_name=state_fileName, 
			path_name=path_name, 
			state_name=state_name
			)

		sides = ['up', 'right', 'down', 'left']
		walls_coordinates = [
			[ [0, 0], [SETT.SCREEN1_WIDTH, 0] ],
			[ [SETT.SCREEN1_WIDTH, 0], [SETT.SCREEN1_WIDTH, SETT.SCREEN1_HEIGHT] ],
			[ [SETT.SCREEN1_WIDTH, SETT.SCREEN1_HEIGHT], [0, SETT.SCREEN1_HEIGHT] ],
			[ [0, SETT.SCREEN1_HEIGHT], [0, 0] ],
		]
		
		# Set walls
		self.walls = []
		for walls_coordinates, side in zip(walls_coordinates, sides):
			self.walls.append( Wall(walls_coordinates[0], walls_coordinates[1], side=side) )
		
		self.shapes = self.particles + self.walls
		
		pygame.mixer.init()
		self.collideSound = pygame.mixer.Sound(f"{PATH_SOUNDS_DIR}/ball-hit-sound.wav")

		# If no recorder is defined it is None by default
		self._record_active = SETT.RECORD_ACTIVE
		self.recorders = []
		self.init_time = init_time
		self.time = init_time

		self.pause = False
		self.quit = False
		
	def loadState(
		self, file_name='initState-random.json', 
		path_name='InitialStates', 
		state_name='random'
		)->None:
		self.state_name = state_name
		file = open(f'{path_name}/{file_name}', "r")
		# file = open("InitialStates/initState-electricTest1.json", "r")
		particles_dic = json.load(file)
		file.close()
		for i, particle_state in particles_dic.items():
			self.particles.append(
				Particle(particle_state["init_pos"], particle_state["init_vel"], particle_state["radius"], index=i) 
			)
		self.num_particles = len(self.particles)

	def saveState(
		self, file_name='savedState-random_null.json', path_name='SavedStates'
		)->None:
		data_dic = {}
		for i, particle in enumerate(self.particles):
			data_dic[str(i)] = {
				"init_pos": list(particle.pos),
				"init_vel": list(particle.vel),
				"radius": particle.radius
			}

		# if path does'nt exist, create it.
		if not os.path.exists(path_name):
			os.mkdir(path_name)	
		
		# dump data to the file
		file = open(f'{path_name}/{file_name}', "w")
		json.dump(data_dic, file, indent=4)
		file.close()

	def playSound(self, activate=SETT.SOUND_ON):
		if activate:
			pygame.mixer.Sound.play(self.collideSound)
			pygame.mixer.music.stop()

	def setRecorder(self, recorder=None):
		if recorder is not None:
			self.recorders.append(recorder)
		else:
			raise Exception(f"initRecorder() function needs 1 argument. 0 was given.")
	
	def checkUserInput(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[K_x]):
					self.pause = True
					self.quit = True
				elif event.key == pygame.K_p:
					self.pause = not self.pause


	def run(self)->None:
		collision = collisionOccur = False
		timeText.update(self.time)
		fpsText.setText(f'fps: {int(self.clock.get_fps())}')
		time_arr = []
		ndt_steps = SETT.N_DT_STEPS
		iteration = 0

		while True:
			self.checkUserInput()
			
			# Draw only every dt_steps in dt
			if not iteration%ndt_steps:
				drawManager.drawAll(self.shapes)	
				drawManager.drawText(timeText)
				drawManager.drawText(fpsText)
				if (self.recorders != []):
					drawManager.plot2D(time_arr, self.recorders, title="Energies")
				self.clock.tick(SETT.FPS)
				drawManager.update()
				
			
			if not self.pause:
				
				# Record using each recorder object
				if (self.recorders != [] and self._record_active):
					if self.time <= self.recorders[0].fin_time:
						time_arr.append(self.time)
						for recorder in self.recorders:
							physical_attribute = 0
							for particle in self.particles:
								# physical_attribute += particle.getAttribute(recorder.record_attribute)
								physical_attribute += particle.__getattribute__(recorder.record_attribute)
							recorder.record_arr.append(physical_attribute)
						

				# Kinematics
				for particle in self.particles:
					if collisionOccur:
						particle.moveByMomentum()
					else:
						particle.moveFree(method_name='verlet')
				
				# Interactions

				# Reset all forces applied on the particle, before recalculating.
				for particle in self.particles:
					particle.resetForces()			
				collisionOccur = False

				# Gravity interaction
				for particle in self.particles:
					interactions.applyGravity(particle)

				# Wall interactions
				for wall in self.walls:
					for particle in self.particles:
						collision = colDetect.detectCollision(particle, wall)
						if collision and not all(particle.atRest):
							# particle.stepBack()
							interactions.FindTrajectory(wall, particle)
							interactions.updateMomentum(wall, particle)
							self.playSound()
							# print("puk")
							collisionOccur = True

				# Particles interactions
				for i in range(self.num_particles):
					indices_potential_coll = interactions.findNeighbors(i, self.particles, length=2)
					# for j in range(i+1, self.num_particles):
					for j in indices_potential_coll:

						# Apply Electric Force between the particles
						interactions.applyElectricForce(self.particles[i], self.particles[j])

						collision = colDetect.detectCollision(self.particles[i], self.particles[j])
						both_at_rest = all(self.particles[i].atRest) and all(self.particles[j].atRest)
						if collision and not both_at_rest:
							# particle.stepBack()
							# print(self.particles[i].index, self.particles[j].index)
							interactions.FindTrajectory(self.particles[i], self.particles[j])
							interactions.updateMomentum(self.particles[i], self.particles[j])
							self.playSound()
							# print("puk")
							collisionOccur = True

				# update time
				# if not self.time%4:
				timeText.update(self.time)
				fpsText.setText(f'fps: {int(self.clock.get_fps())}')
				self.time += SETT.DT
				iteration += 1
				
			if self.quit:
				break

		pygame.quit()
		if SETT.SAVE_TO_FILE:
						
			# make current time as a a string (with 2 decimals)
			time_str = '{:.2f}'.format(round(self.time, 2)).replace('.', '_')

			# define the file's name
			file_name = f'savedState-{self.state_name}-time_{time_str}.json'

			# define the file's local path
			path_local = f'SavedStates/{self.state_name}'

			self.saveState(
				file_name=file_name, path_name=path_local
				)
			self.lastSaved_fileName = f'{path_local}/{file_name}'

			return

		sys.exit()


if __name__ == '__main__':
	sim1 = Simulation1()
	
	# Set recorders
	init_time, fin_time = 0, 10000*DT
	
	if SETT.RECORD_ACTIVE:
		recorder_Kenergy = Recorder()
		recorder_Kenergy.record("kinetic_energy", init_time, fin_time)
		recorder_Penergy = Recorder()
		recorder_Penergy.record("potential_energy", init_time, fin_time)
		recorder_Totenergy = Recorder()
		recorder_Totenergy.record("total_energy", init_time, fin_time)

		sim1.setRecorder(recorder_Kenergy)
		sim1.setRecorder(recorder_Penergy)
		sim1.setRecorder(recorder_Totenergy)
	sim1.run()
	
	print("Done")
	energy = recorder_energy.record_arr.copy()
	time = [n*SETT.DT for n in range(len(energy))]
	print(time)
	print(energy)