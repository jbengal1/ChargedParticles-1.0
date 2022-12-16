from math import sqrt, acos, atan, pi
import numpy as np
from numpy.linalg import norm
import json
import Visualization.Text as Text

from Engine.Settings import Settings as SETT
from MathUtilities.Vector import Vec2

LINE_THICKNESS = 5

class Circle(object):
    def __init__(
        self, 
        pos = [SETT.SCREEN1_WIDTH/2, SETT.SCREEN1_HEIGHT/2], 
        radius=10, thickness=LINE_THICKNESS, 
        name="defaultCircle"):

        self.name = name
        self.pos = pos
        self.radius = radius
        self.thickness = thickness
        self.draw_coordinates = SETT.DRAW_COORDINATES

        self.cross_point = None

    def __str__(self):
        self.directory = {
            "name": self.name,
            "pos": self.pos,
            "radius": self.radius,
            "thickness": self.thickness        
            }
        return json.dumps(self.directory, indent=4)
    
    def drawCoordinates(self, screen, draw=SETT.DRAW_COORDINATES):
        self.draw_coordinates = draw

        if self.draw_coordinates:
            # Create text objects
            self.text_coordinates = Text.Coordinates(self.pos[0], self.pos[1])

            # Draw text objects on the screen
            self.text_coordinates.draw(screen)
    
    def checkPointIn(self, point) -> bool:
        rel_center_vector = np.array(point) - np.array(self.pos)
        return norm(rel_center_vector) <= self.radius

    def checkPointOn(self, point) -> bool:
        # Check if the calculated point on the circle
        p1, p2 = self.pos[0], self.pos[1]
        x, y = point[0], point[1]
        # generally there are two y solutions for a given x..
        # we want the solution which gives abs(y_sol - y) = 0
        solutions = [
            abs(y + ((-1)**n)*sqrt(self.radius**2 - (x-p1)**2) - p2) 
            for n in range(2)
            ]
        
        return min(solutions) <= 0.0001
        # if min(solutions) <= 0.0001:
        #     return True
        # else:
        #     return False
    
    def getCrossPoint(self, line):
        ''' 
        This function returns the cross point 
        of this circle with a given line. 
        '''

        # Set all short named parameters for later calculations.
        a = line.slope
        b = line.y_intersection
        R = self.radius
        p1 = self.pos[0]
        p2 = self.pos[1]

        # Calculate cross point (assuming infinite length line)
        if a == 'inf':
            x_cross = line.p1[0]
        else:
            A = a**2 + 1
            B = 2*(-p1 + a*b - a*p2)
            C = b**2 + p1**2 + p2**2 - R**2 - 2*b*p2
            if B**2 >= 4*A*C:
                x_cross = np.array([
                    (-B + ((-1)**n)*sqrt(B**2 - 4*A*C))/(2*A) for n in range(2)
                    ])
            else:
                return None
        
        y_cross = line.getLineFunction(x_cross)
        if y_cross is not None:
            # create 2 vectors (2-dim array):
            # from line's initial point to each of the 2 crossing points
            rel_vectors = np.array([x_cross, y_cross]).T - np.array(line.p1)

            # calculate each of the 2 norms ()
            rel_vectors_lengths = norm(rel_vectors, axis=1)
            
            # choose the closest point to lines initial point.
            min_index = np.argmin(rel_vectors_lengths) 
            return list(np.array([x_cross, y_cross]).T[min_index])
        else:
            return None

    def calculateDistanceTo(self, point):
        if type(point) is not Vec2:
            return (self.pos - Vec2(point)).getNorm()
        else: 
            return (self.pos - point).getNorm()