import json
import numpy as np
from math import sqrt
from random import random

project_dir_path = '/home/yonatan/python_projects/PySimulations/ChargedParticles-1.0'
init_state_dir = "InitialStates"

if __name__=='__main__':
    import sys
	# Add main directory to path
    sys.path.insert(0, project_dir_path)
    from Engine.Settings import *


particles_dic = {}
max_vel = 10
min_radius = 4
max_radius = 4
N_Particles = 3

def checkOverlap(p1, r1, p2, r2):
    distance = np.array(p1) - np.array(p2)
    distance = np.linalg.norm(distance)
    return distance <= r1 + r2

def checkWallOverlap(p, r):
    if p[0] + r >= SCREEN1_WIDTH:
        return True
    elif p[0] - r <= 0:
        return True
    elif p[1] + r >= SCREEN1_HEIGHT:
        return True
    elif p[1] - r <= 0:
        return True
    else:
        return False

def setRandomState(num_particles):
    # Particle 0
    radii = []
    positions = []
    while True:
        radius =  min_radius + random()*(max_radius - min_radius)
        init_pos = [random()*SCREEN1_WIDTH, random()*SCREEN1_HEIGHT]
        if not checkWallOverlap(init_pos, radius):
            break
    
    radii.append(radius)
    positions.append(init_pos)
    init_vel = [max_vel*random(), max_vel*random()]
    # init_vel = [0, 0]        
    particles_dic[str(0)] = {
        "init_pos": init_pos,
        "init_vel": init_vel,
        "radius": radius
    }
    print("Particle 0 is set.") 

    for i in range(1, num_particles):
        overLap = True
        broke = False
        iteration = 0        
        while overLap:
            init_pos = [random()*SCREEN1_WIDTH, random()*SCREEN1_HEIGHT]
            radius =  min_radius + random()*(max_radius - min_radius)

            if not checkWallOverlap(init_pos, radius):
                for r2, pos2 in zip(radii, positions):
                    if checkOverlap(init_pos, radius, pos2, r2):
                        broke = True
                        break
                    iteration += 1 
                if not broke:
                    overLap = False
                print(iteration)
                if iteration >= 1000:
                    break

        radii.append(radius)
        positions.append(init_pos)

        init_vel = [max_vel*random(), max_vel*random()]
        # init_vel = [0, 0]        
        particles_dic[str(i)] = {
            "init_pos": init_pos,
            "init_vel": init_vel,
            "radius": radius
        }
        print(f"Particle {i} is set.") 
    # for i in range(num_particles):
    #     r1, p1 = radii[i], positions[i]
    #     for j in range(i+1, num_particles):
    #         r2, p2 = radii[j], positions[j]
    #         distance = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    #         print(distance <= r1 + r2, distance , r1 + r2)


setRandomState(100)
file = open(f"{project_dir_path}/{init_state_dir}/initState-random.json", "w")
json.dump(particles_dic, file, indent=4)
file.close()