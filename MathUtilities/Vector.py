from math import *

class Vector:
	def __init__(self, array):
		self.vec = array
		self.dim = len(array)

	def getVec(self):
		return self.vec

	def __call__(self):
		return self.vec

	def __str__(self):
		return str(self.vec)


class Vec2(Vector):
	def __init__(self, x, y):
		Vector.__init__(self, [x, y])

	def __add__(self, vec2):
		v1 = self.vec
		try:
			v2 = vec2.getVec()
			return Vec2(v1[0] + v2[0], v1[1] + v2[1])
		except BaseException:
			print(f"Could not add to the object {type(vec2)}.")

	def __sub__(self, vec2):
		v1 = self.vec
		try:
			v2 = vec2.getVec()
			return Vec2(v1[0] - v2[0], v1[1] - v2[1])
		except BaseException:
			print(f"Could not substract to the object {type(vec2)}.")

	def __mul__(self, vec2):
		v1 = self.vec
		try:
			v2 = vec2.getVec()
			return v1[0]*v2[0] + v1[1]*v2[1]
		except:
			scalar = vec2
			return Vec2(v1[0]*scalar, v1[1]*scalar)

	def __rmul__(self, scalar):
		v1 = self.vec
		return Vec2(v1[0]*scalar, v1[1]*scalar)

	def __truediv__(self, scalar):
		try:
			return Vec2(self.vec[0]/scalar, self.vec[1]/scalar)
		except BaseException:
			print(f"Could not divide by the object {type(scalar)}.")

	def __pos__(self):
		return self

	def __neg__(self):
		return Vec2(-self.vec[0], -self.vec[1])

	def __eq__(self, vec2):
		try:
			v2 = vec2.getVec()
			return self.vec[0]==v2[0] and self.vec[1]==v2[1]
		except BaseException:
			print(f"Comparsion of Vec2 to {type(vec2)} is not defined.")
	
	def __len__(self):
		return len(self.vec)
	
	def __getitem__(self, item):
		return self.vec[item]

	def __setitem__(self, item, value):
		self.vec[item] = value

	def __iter__(self):
		return iter(self.vec)
	
	def __contains__(self, item):
		return item in self.vec

	def getNorm(self):
		return sqrt(self.vec[0]**2 + self.vec[1]**2)

	def getTheta(self):
		x = self.vec[0]		
		y = self.vec[1]
		r = self.getNorm()
		# if abs(x)>1e-20:
		if x > 0:
			if y >= 0:
				return atan(y/x)*180/pi
			if y < 0:
				return atan(y/x)*180/pi + 360
		elif x < 0:
			return atan(y/x)*180/pi + 180
		else:
			if y > 0:
				return 90
			if y < 0:
				return 270
		# else:
		# 	if y>0:
		# 		return 90
		# 	elif y<0:
		# 		return 270
		# 	else:
		# 		return 0

class Matrix:
	def __init__(self, mat=[[]]):
		self.mat = mat
		self.dim = (len(mat), len(mat[0]))
		self.N = len(mat)
		self.M = len(mat[0])

	def setMatrix(self, mat=[[]]):
		self.mat = mat
		self.dim = (len(mat), len(mat[0]))
		self.N = len(mat)
		self.M = len(mat[0])

	def __call__(self):
		return self.mat

	def __str__(self):
		return str(self.mat)

	def __mul__(self, vector):
		try:
			if vector.dim == self.N:
				new_vector = [0]*vector.dim
				for n in range(self.N):
					for m in range(self.M):
						new_vector[n] += self.mat[n][m]*vector[m]
				
				if vector.dim==2:
					return Vec2(new_vector[0], new_vector[1])
				else:
					return Vector(new_vector)

			else:
				print(f"Matrix row and vector must be of the same dimension.")
				print(f"Matrix dim is {self.dim} and vector dim is {vector.dim}.")
		
		except BaseException:
			print(f"Can't use multiplie matrix by type {type(vector)}")
			print(f"Matrix multiplication requires a vector or a matrix with the appropriate dimension.")
			

def Rotation2(vector, angle):
	angle *= pi/180
	rotation_mat = Matrix([
		[cos(angle), -sin(angle)],
		[sin(angle), cos(angle)]
	])
	return rotation_mat*vector


if __name__ == '__main__':
	a = Vec2(1,2)
	b = Vec2(3,4)
	c = a + b
	d = a - b
	e = a/2
	n = a/a.getNorm()
	print(a, b, c, d)
	print(e) 
	print(+a, -a)
	print(a/b)
	print(n, n.getNorm())

	for x in a:
		print(x)

	print(1 in a)
	x = Vec2(1, 0)
	print(Rotation2(x, 180))
	for n in range(8):
		v = Vec2( cos(2*pi*n/8), sin(2*pi*n/8) )
		print(n, v, v.getTheta())

	# check more rotations
	n += 1
	v = Vec2( cos(2*pi*n/8), sin(2*pi*n/8) )
	print(n, v, v.getTheta())