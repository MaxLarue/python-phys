#	ADT module
#	définit les abstract data types qui pourront être utilisés dans tout la programme
#
#
#
#
#
#

EPSILON = 0.000001

def floatCmp(one, two):
	return abs(one-two) < EPSILON

def checkParamType(arg, types):
	ok = False
	for t in types:
		ok = isinstance(arg, t) or ok
	return ok

def clampStr(it, nb=7):
	return it[:min(nb, len(it))]

class ADTException(Exception):
	""" Exception commune à touts les ADT """
	def __init__(self, message):
		super(ADTException, self).__init__(message)

class Vec2Exception(ADTException):
	""" Exception pour les Vec2 """
	def __init__(self, message):
		super(Vec2Exception, self).__init__(message)

class Vec2(object):
	"""Vecteur à 2 composantes (x, y). Objet immutable (comme tuple)"""
	__slots__ = ["__x", "__y"]
	def __init__(self, *arg):
		"""
			Constructeur
				Vec2() : vecteur (0, 0)
				Vec2((0, 0))
				Vec2([0, 0])
				Vec2("Vec2(0, 0)")
				Vec2(0, 0)
			Lève une Vec2Exception en cas de problème de paramètres
		"""
		super(Vec2, self).__init__()
		try:
			if(len(arg) == 0):
				self.__x = 0.0
				self.__y = 0.0
			elif(len(arg) == 1):
				if(isinstance(arg[0], tuple) or isinstance(arg[0], list)):
					self.__x = float(arg[0][0])
					self.__y = float(arg[0][1])
				elif(isinstance(arg[0], str)):
					string = arg[0].replace(" ", "")
					string = string[4:]
					string = string.replace("(", "").replace(")", "")
					coord = string.split(",")
					self.__x = float(coord[0])
					self.__y = float(coord[1])
				else:
					raise Vec2Exception("Unconsistent arg for __init__ : "+repr(arg))
			elif(len(arg) == 2):
				self.__x = float(arg[0])
				self.__y = float(arg[1])
			else:
				raise Vec2Exception("Unconsistent arg for __init__ : "+repr(arg))
		except Exception as e:
			raise Vec2Exception("Exception in __init__ : "+str(e))

	def __size(self):
		#Privé, calcule la taille du vecteur
		return self.__sqSize()**(1/2)

	def __sqSize(self):
		#Privé, calcule le carré de la taille du vecteur
		return (self.__x*self.__x + self.__y*self.__y)

	def __chckOperand(self, operand, types, opName="unknown operation"):
		if(not checkParamType(operand, types)):
			raise Vec2Exception("Bad operand in "+opName+" : "+repr(operand)+" must be of one of those types : "+repr(types))

	#
	#Getters Publics
	#

	def get(self):
		#renvoie le vecteur sous forme d'un tuple de float (float x, float y)
		return (self.__x, self.__y)

	def x(self):
		#renvoie la coordonnée x du vecteur sous forme de float
		return self.__x

	def y(self):
		#renvoie la coordonnée y du vecteur sous forme de float
		return self.__y

	def getI(self):
		#renvoie le vecteur sous forme de tuple de int
		return (int(self.__x), int(self.__y))

	def xI(self):
		#renvoie la coordonnée x sous forme de int
		return int(self.__x)

	def yI(self):
		#renvoie la coordonnée y sous forme de int
		return int(self.__y) 

	#
	#	Constructeur de copie
	#
	def getCopy(self):
		return Vec2(self.__x, self.__y)

	def __eq__(self, other):
		return self.x() == other.x() and self.y() == other.y()

	#
	#	Opérations
	#
	def __add__(self, other):
		#addition vectorielle, renvoie un vecteur
		self.__chckOperand(other, [Vec2], "add")
		return Vec2(self.__x+other.x(), self.__y+other.y())

	def __sub__(self, other):
		#soustraction vectorielle, renvoie un vecteur
		self.__chckOperand(other, [Vec2], "sub")
		return Vec2(self.__x - other.x(), self.__y - other.y())

	def __truediv__(self, num):
		#division par un scalaire, renvoie un vecteur
		self.__chckOperand(num, [float, int], "div")
		if(num == 0):
			raise Vec2Exception("Vec2 __div__ : Division by zero error")
		return Vec2(self.__x/num, self.__y/num)

	def __mul__(self, num):
		#multiplication par un scalaire, renvoie un vecteur
		#attention Vec2 * scalaire	OK
		#		   scalaire * Vec2  NOK
		self.__chckOperand(num, [float, int], "mul")
		return Vec2(self.__x*num, self.__y*num)

	def scalar(self, other):
		#produit scalaire de deux vecteurs, renvoie un float
		self.__chckOperand(other, [Vec2], "scalar")
		return self.__x*other.x() + self.__y*other.y()

	def __eq__(self, other):
		return floatCmp(self.x(), other.x()) and floatCmp(self.y(), other.y())

	#
	#	Spéciaux
	#
	def unit(self):
		#renvoie un vecteur unitaire de même sens et de même direction que self
		if(floatCmp(self.__sqSize(), 0)):
			return Vec2(0, 0)
		else:
			return self/self.__size()

	def size(self):
		#renvoie la taille du vecteur
		return self.__size()

	def sqSize(self):
		#renvoie la taille au carré du vecteur
		return self.__sqSize()

	def __str__(self):
		return "V2("+clampStr(str(self.__x))+", "+clampStr(str(self.__y))+")"

	def __repr__(self):
		return str(self)


class PQueueException(ADTException):
	def __init__(self, message):
		"""
			Exception pour les PQueue
		"""
		super(PQueueException, self).__init__(message)



class PQueue(object):
	"""
	Priority Queue implémentée à l'aide d'un heap
	"""
	def __init__(self, rev=False):
		super(PQueue, self).__init__()
		self.__heap = []
		if(not rev):
			self.__lw = lambda x, y: x < y
			self.__hg = lambda x, y: x > y
		else:
			self.__lw = lambda x, y: x > y
			self.__hg = lambda x, y: x < y

	def __parent(self, index):
		if(index % 2 == 0):
			return (index - 2 ) // 2
		else:
			return (index - 1) // 2

	def __left(self, index):
		return 2 * index + 1

	def __right(self, index):
		return 2 * index + 2

	def __swap(self, one, two):
		self.__heap[one] , self.__heap[two] = self.__heap[two], self.__heap[one]

	def __exist(self, index):
		return index >= 0 and index < len(self.__heap) 

	def __siftUp(self, index):
		#fait remonter l'élément à l'indice index à la bonne place via sa prioritée
		parentIndex = self.__parent(index)
		if(self.__exist(parentIndex) and self.__lw(self.__heap[parentIndex][0], self.__heap[index][0])):
			self.__swap(index, parentIndex)
			self.__siftUp(parentIndex)


	def __siftDown(self, index):
		leftIndex = self.__left(index)
		rightIndex = self.__right(index)
		if(not self.__exist(leftIndex)):
			pass
		elif(not self.__exist(rightIndex)):
			if(self.__hg(self.__heap[leftIndex][0], self.__heap[index][0])):
				self.__swap(index, leftIndex)
				self.__siftDown(leftIndex)
		else:
			if(self.__hg(self.__heap[leftIndex][0], self.__heap[rightIndex][0])):
				if(self.__hg(self.__heap[leftIndex][0], self.__heap[index][0])):
					self.__swap(leftIndex, index)
					self.__siftDown(leftIndex)
			else:
				if(self.__hg(self.__heap[rightIndex][0], self.__heap[index][0])):
					self.__swap(rightIndex, index)
					self.__siftDown(rightIndex)


	#
	#	Public interface
	#

	def pop(self):
		if(self.empty()):
			raise PQueueException("pop alors que PQueue vide")
		if(len(self.__heap) == 1):
			return self.__heap.pop()
		#else
		self.__swap(0, len(self.__heap)-1)
		ret = self.__heap.pop(len(self.__heap)-1)
		if(not self.empty()):
			self.__siftDown(0)
		return ret

	def empty(self):
		return len(self.__heap) == 0

	def push(self, prior, elem):
		self.__heap.append((prior, elem))
		self.__siftUp(len(self.__heap)-1)

	def size(self):
		return len(self.__heap)

class GraphException(Exception):
	def __init__(self, message):
		"""
			Exception pour les Graphes
		"""
		super(GraphException, self).__init__(message)


class Vertex(object):
	def __init__(self, key):
		self.__key = key
		self.__connections = {}

	def addNeighbor(self, otherKey, weight):
		self.__connections[otherKey] = weight

	def delNeighbor(self, otherKey):
		try:
			del self.__connections[otherKey]			
		except Exception as e:
			raise GraphException(str(e))

	def getConnections(self):
		cons = []
		for k in  self.__connections.keys():
			cons.append((k, self.__connections[k]))
		return cons

	def isNeighbor(self, otherKey):
		return otherKey in self.__connections.keys()

	def getKey(self):
		return self.__key

	def getWeight(self, otherKey):
		try:
			ret = self.__connections[otherKey]
			return ret
		except Exception as e:
			raise GraphException(str(e))

	def __str__(self):
		return str(self.__key+" : "+str([k for k in self.__connections.keys()]))


class Graph(object):
	def __init__(self):
		super(Graph, self).__init__()
		self.__vertices = {}
		self.__verticeNum = 0

	def addVertex(self, vert):
		if(not vert in self.__vertices.keys()):
			self.__verticeNum += 1
			self.__vertices[vert.getKey()] = vert

	def addEdge(self, fromVert, toVert, weight):
		if(not (fromVert in self.__vertices and toVert in self.__vertices)):
			raise GraphException("Trying to add edge from "+str(fromVert)+" to "+str(toVert))
		#else
		self.__vertices[fromVert].addNeighbor(toVert, weight)
		self.__vertices[toVert].addNeighbor(fromVert, weight)
	
	def getVertex(self, vertKey):
		try:
			return self.__vertices[vertKey]
		except Exception as e:
			raise GraphException(str(e))

	def getVerticesKeys(self):
		return self.__vertices.keys()

	def isIn(self, vertKey):
		return vertKey in self.__vertices.keys()

	def removeVertex(self, vertKey):
		if(self.isIn(vertKey)):
			for k in self.__vertices.keys():
				try:
					self.__vertices[k].delNeighbor(vertKey)
				except:
					pass
			del self.__vertices[k]
			self.__verticeNum -= 1

	def size(self):
		return self.__verticeNum

	def removeEdge(self, fromV, toV):
		if(not self.isIn(fromV)):
			raise GraphException("Tried to remove edge from non existing vertex : "+str(fromV))
		if(not self.isIn(toV)):
			raise GraphException("Tried to remove edge to non existing vertex : "+str(toV))
		#else
		self.__vertices[fromV].delNeighbor(toV)
		self.__vertices[toV].delNeighbor(fromV)

	def getNeighbors(self, vKey):
		try:
			return self.__vertices[vKey]
		except Exception as e:
			raise GraphException(str(e))

def djikstra(graph, startKey, stopKey):
	frontier = PQueue(True)
	frontier.push(0, startKey)
	cameFrom = {}
	cost = {}
	cameFrom[startKey] = None
	cost[startKey] = 0
	while(not frontier.empty()):
		current = frontier.pop()[1]
		if(current == stopKey):
			break
		neighbsKeys = [e[0] for e in graph.getNeighbors(current).getConnections()]
		neighbs = [graph.getVertex(i) for i in neighbsKeys]
		for n in neighbs:
			newCost = cost[current] + n.getWeight(current)
			if(not n.getKey() in cost.keys() or newCost < cost[n.getKey()]):
				cost[n.getKey()] = newCost
				frontier.push(newCost, n.getKey())
				cameFrom[n.getKey()] = current
	return cameFrom

def buildPathFromDjikstra(cameFrom, start, end):
	path = []
	path.append(end)
	while(path[0] != start):
		path = [cameFrom[path[0]]] + path
	return path


class OrderedList(object):
	#liste triée en place, les éléments doivent implémenter les opérateurs de comparaison
	#ordre croissant
	def __init__(self, l=[]):
		self.__l = []
		self.__actIter = -1
		for e in l:
			self.add(e)

	def __dicho(self, elem, lower=0, upper=-2):
		if(upper == -2):
			upper = len(self)
		if(upper <= lower):
			return lower
		else:
			halfW = (upper-lower-1)//2
			pivot = lower + halfW
			if(elem > self.__l[pivot]):
				return self.__dicho(elem, pivot+1, upper)
			else:
				return self.__dicho(elem, lower, pivot)
		

	def add(self, elem):
		#ajoute l'élément elem
		self.__l.insert(self.__dicho(elem), elem)

	def isIn(self, elem):
		i = self.__dicho(elem)
		return i >= 0 and i < len(self) and self.__l[i] == elem

	def remove(self, elem):		
		#enlève l'élément elem
		if(self.isIn(elem)):
			del self.__l[self.__dicho(elem)]

	def removeAt(self, index):
		#enlève l'élement a l'index index
		del self.__l[index]

	def __len__(self):
		#renvoie la longueur
		return len(self.__l)

	def __iter__(self):
		#renvoie un itérateur
		self.__actIter = 0
		return self

	def __next__(self):
		#prochaine itération
		if(self.__actIter >= 0 and self.__actIter < len(self)):
			self.__actIter += 1
			return self.__l[self.__actIter - 1]
		else:
			raise StopIteration

	def __getitem__(self, key):
		return self.__l[key]

	def __repr__(self):
		return repr(self.__l)
