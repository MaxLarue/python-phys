import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

import math

import pdb

from Basic.ADT import *

PI = math.pi

class Shape(object):
	#forme générale	!!!!!!!!!convexe

	def __init__(self, points=[]):
		self.__points = []
		if(len(points) > 0):
			if(isinstance(points[0], tuple) or isinstance(points[0], list)):
				for p in points:
					self.__points.append(Vec2(p))
			else:
				self.__points = points
		else:
			self.__points = []
		if(len(self.__points) == 0):
			self.__normals = []
			self.__center = Vec2()
			self.__radius = 0.0
		else:
			self.__normals = self.__computeNormals()
			self.__center = self.__computeCenter()
			self.__radius = self.__computeRadius()

	def __computeNormals(self):
		norms = []
		for i in range(len(self.__points)):
			normal = (self.__points[i] - self.__points[i-1]).unit()
			normal = Vec2(normal.y(), normal.x())
			normal = Vec2(normal.x()*-1, normal.y())
			norms.append(normal)
		return norms

	def __computeCenter(self):
		summed = Vec2()
		for p in self.__points:
			summed = summed + p
		summed = Vec2(summed.x()/len(self.__points), summed.y()/len(self.__points))
		return summed

	def __computeRadius(self):
		fartestDst = 0
		for p in self.__points:
			dst = (p - self.getCenter()).size()
			if(dst > fartestDst):
				fartestDst = dst
		return fartestDst

	def getNormals(self):
		#renvoie les normales
		return self.__normals

	def getCenter(self):
		#renvoie le centre
		return self.__center

	def getRadius(self):
		#renvoie le rayon
		return self.__radius

	def getTransPoints(self, trans):
		#renvoie une liste des points comme si la forme avait été déplacé selon trans
		ret = []
		for p in self.__points:
			ret.append(p+trans)
		return ret
	
	def getCenterTrans(self, trans):
		#idem pour centre
		return self.__center+trans

	def nbOfPoints(self):
		#renvoie le nombre de points du polygone
		return len(self.__points)

	def nbofEdges(self):
		#renvoie le nombre de cotés du polygone
		return len(self.__points)-1

	def projectOn(self, axis, trans):
		points = self.getTransPoints(trans)
		ret = []
		for p in points:
			ret.append(p.scalar(axis))
		return (min(ret), max(ret))

	def getArea(self):
		if(len(self.__points) < 3 ):
			return 0
		newP = self.__points[:]+[self.__points[0]]
		summed = 0
		for p in range(len(self.__points)):
			summed += newP[p].y()*newP[p+1].x() - newP[p].x()*newP[p+1].y()
		return abs(summed)/2

class AABB(Shape):
	def __init__(self, width, height):
		point = [
			Vec2(-1*width/2, height/2),
			Vec2(width/2, height/2),
			Vec2(width/2, -1*height/2),
			Vec2(-1*width/2, -1*height/2),
		]
		super().__init__(point)

	def getNormals(self):
		return [Vec2(1, 0), Vec2(0, 1)]

def SATOverlap(proj1, proj2):
	if(proj1[0] < proj2[0]):
		return proj1[1] - proj2[0]
	else:
		return proj2[1] - proj1[0]

def SAT(shape1, shape2, pos1, pos2):
	#pdb.set_trace()
	axis1 = shape1.getNormals() 
	axis2 = shape2.getNormals()
	overlaps = []
	j = 0
	for a in axis1+axis2:
		over = SATOverlap(shape1.projectOn(a, pos1), shape2.projectOn(a, pos2))
		if(over > 0):
			overlaps.append((over, a, j))
		else:
			return None
		j += 1
	#no sa
	ret = {"one" : shape1, "two" : shape2}
	minIndex = 0
	minD = overlaps[0][0]
	axis = overlaps[0][1]
	for i in range(len(overlaps)):
		if(overlaps[i][0] < minD):
			minD = overlaps[i][0]
			axis = overlaps[i][1]
			minIndex = i
	#création manifold
	ret["axis"] = axis
	ret["magnitude"] = minD
	return ret

def preCollide(shape1, shape2, pos1, pos2):
	dstBtw = (shape1.getCenter() + pos1) - (shape2.getCenter() + pos2)
	sqrDst = dstBtw.x()**2 + dstBtw.y()**2
	return (shape1.getRadius()+shape2.getRadius())**2 > sqrDst 

def getRegPolygon(nbOfPoints, radius, at=None):
	points = []
	edgeLen = (radius*PI/(2*PI/nbOfPoints)) - (2*radius)
	alpha = 2*PI/nbOfPoints
	for i in range(nbOfPoints):
		newP = Vec2(radius*math.cos(alpha*i), radius*math.sin(alpha*i))
		points.append(newP)
	return Shape(points)


