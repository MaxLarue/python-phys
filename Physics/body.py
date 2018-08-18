from Shape import *

MATERIALS = {
"Rock" :       
	{
	"Density" : 0.6,  "Restitution" : 0.1, "StaticFriction" : 0.9, "DynamicFriction" : 0.8
	},
"Wood" :       
	{
	"Density" : 0.3,  "Restitution" : 0.2, "StaticFriction" : 0.8, "DynamicFriction" : 0.7
	},
"Metal" :      
	{
	"Density" : 1.2,  "Restitution" : 0.05, "StaticFriction" : 0.5, "DynamicFriction" : 0.5
	},
"BouncyBall" : 
	{
	"Density" : 0.3,  "Restitution" : 0.8, "StaticFriction" : 0.1, "DynamicFriction" : 0.1
	},
"SuperBall" :  
	{
	"Density" : 0.3,  "Restitution" : 0.95, "StaticFriction" : 0.1, "DynamicFriction" : 0.01
	},
"Pillow" :     
	{
	"Density" : 0.1,  "Restitution" : 0.2, "StaticFriction" : 0.4, "DynamicFriction" : 0.4
	},
"Static" :     
	{
	"Density" : 0.0,  "Restitution" : 0.4, "StaticFriction" : 0.8, "DynamicFriction" : 0.8
	}
}

#optimisation pythSolve (pré calculation des résultats)
PRE_COMPUTED_STATIC_FRICTION = {}
for m1 in MATERIALS.keys():
	newRet = {}
	for m2 in MATERIALS.keys():
		newRet[m2] = (MATERIALS[m1]['StaticFriction']**2+MATERIALS[m2]["StaticFriction"]**2)**(1/2)
	PRE_COMPUTED_STATIC_FRICTION[m1] = newRet

PRE_COMPUTED_DYNAMIC_FRICTION = {}
for m1 in MATERIALS.keys():
	newRet = {}
	for m2 in MATERIALS.keys():
		newRet[m2] = (MATERIALS[m1]['DynamicFriction']**2+MATERIALS[m2]["DynamicFriction"]**2)**(1/2)
	PRE_COMPUTED_DYNAMIC_FRICTION[m1] = newRet

REST_FRICTION_THRESHOLD = 0.00001

class Body:
	def __init__(self, shape, material):
		self.__shape = shape			#toutes les formes appartenant au body
		self.__pos = Vec2(0, 0) 				#position du body
		self.__material = MATERIALS[material]			#materiaux du body
		self.__matName = material
		self.__totalArea = shape.getArea()
		self.__mass = self.__totalArea*self.__material["Density"]
		self.__invMass = 1/self.__mass if self.__mass != 0 else 0         #masse inverse du body
		self.__speed = Vec2(0, 0) 			#vitesse du body
		self.__force = Vec2(0, 0)   			#force totale sur le body

	def collide(self, other):
		#renvoie un manifold si ce body est en collision avec l'autre body
		ret = SAT(self.__shape, other.getShape(), self.__pos, other.getPos())
		if(not ret is None):
			ret["oneBody"] = self
			ret["twoBody"] = other
		return ret

	def preCollide(self, other):
		return preCollide(self.getShape(), other.getShape(), self.getPos(), other.getPos())

	def separateVector(self, manifold):
		if(self is manifold["oneBody"]):
			this = manifold["oneBody"]
			other = manifold["twoBody"]
		elif(self is manifold["twoBody"]):
			this = manifold["twoBody"]
			other = manifold["oneBody"]
		else:
			return None
		ret = manifold["axis"]*(manifold["magnitude"]*1.000001)
		if(ret.scalar((this.getPos()+this.getShape().getCenter()) - (other.getPos()+other.getShape().getCenter())) < 0):
			ret = ret * -1
		return ret


	def integrate(self, dt):
		#déplace le body sur l'interval dt
		if(not floatCmp(self.getInvMass(), 0)):
			self.__speed += self.__force*self.__invMass*dt
			self.__pos += self.__speed*dt

	def getPos(self):	
		#renvoie la position du body
		return self.__pos

	def zeroForce(self):	
		#remet la force à zéro
		self.__force = Vec2(0, 0)

	def addForce(self, force):	
		#applique une force(impulsive)
		self.__force += force

	def teleport(self, at):
		#déplace instantanément l'objet à l'endroit at
		self.__pos = at.getCopy()

	def getMat(self):
		return self.__matName

	def getMass(self):
		return self.__mass

	def getInvMass(self):
		return self.__invMass

	def getDensity(self):
		return self.__material["Density"]

	def getRestitution(self):
		return self.__material["Restitution"]

	def getShape(self):
		return self.__shape

	def getVelocity(self):
		return self.__speed

	def getStaticFriction(self):
		return self.__material["StaticFriction"]

	def getDynamicFriction(self):
		return self.__material["DynamicFriction"]

	def applyImpulse(self, impulse):
		self.__speed += impulse

	def speedAlongNormal(self, relativeSpeed, normal):
		return relativeSpeed.scalar(normal)

	def relativeSpeed(self, other):
		return other.getVelocity() - self.__speed

	def resolutionImpulse(self, other, restitution, relativeSpeed, separateVec):
		normal = separateVec.unit()*-1
		relAlongNormal = self.speedAlongNormal(relativeSpeed, normal)
		if(relAlongNormal > 0):
			return Vec2(0, 0)
		j = normal*relAlongNormal*(1/(self.getInvMass() +other.getInvMass())*(1+restitution))
		return j

	def minRestitution(self, other):
		return min(self.getRestitution(), other.getRestitution())

	def positionalCorrection(self, other, separateVec):
		percent = 0.2
		slop = 0.01
		if(not ((floatCmp(self.getInvMass(), 0) and floatCmp(other.getInvMass(), 0)))):
			if(separateVec.size() > slop):
				correction = separateVec*percent/(self.getInvMass()+other.getInvMass())
				self.__pos += correction*self.getInvMass()

	def frictionImpulse(self, other, separateVec, impulseSize):
		frictionDir = (self.getVelocity()).unit()
		normal = Vec2(frictionDir.y(), -1*frictionDir.x())
		if(normal.scalar(separateVec) > 0):
			normal = normal * -1
		#projection de l'impulsion sur la normale
		frictionMod = normal.scalar(separateVec)
		#multiplication par mu
		#staticFriction = frictionMod*pythSolve(self.getStaticFriction(), other.getStaticFriction())
		# optimisation pre-calcul
		staticFriction = frictionMod*PRE_COMPUTED_STATIC_FRICTION[self.getMat()][other.getMat()]
		#application d'un seuil
		# if(staticFriction < REST_FRICTION_THRESHOLD):
		# 	return Vec2(0, 0)
		if(staticFriction < separateVec.scalar(self.getVelocity())):
			return frictionDir*staticFriction
		else:
			#return frictionDir*frictionMod*pythSolve(self.getDynamicFriction(), other.getDynamicFriction())
			return frictionDir*frictionMod*PRE_COMPUTED_DYNAMIC_FRICTION[self.getMat()][other.getMat()]



def pythSolve(a, b):
	return (a**2 + b**2)**(1/2)

def cullPairs(l):
	pairs = {}
	culled = []
	for coll in l:
		#optimisation : pas de paires static/static
		if(((not floatCmp(coll["oneBody"].getInvMass(), 0)) or (not floatCmp(coll["twoBody"].getInvMass(), 0)))):
			cull = True
			if(not coll["oneBody"] in pairs.keys()):
				pairs[coll["oneBody"]] = [coll["twoBody"]]
				if(not coll["twoBody"] in pairs.keys()):
					pairs[coll["twoBody"]] = [coll["oneBody"]]
				else:
					pairs[coll["twoBody"]].append(coll["oneBody"])
			elif(coll["oneBody"] in pairs.keys()):
				if(not coll["twoBody"] in pairs[coll["oneBody"]]):
					pairs[coll["oneBody"]].append(coll["twoBody"])
				else:
					cull = False
			else:
				cull = False
			if(cull):
				culled.append(coll)
	return culled

def resolveCollisions(colls):
	for coll in colls:
		resolveCollision(coll)
		
def resolveCollision(coll):
	if((not floatCmp(coll["oneBody"].getInvMass(), 0)) or (not floatCmp(coll["twoBody"].getInvMass(), 0)) ):
		restitution = coll["oneBody"].minRestitution(coll["twoBody"])
		#optimisation : ne pas résoudre les collisions pour les objets statiques
		if(not floatCmp(coll["oneBody"].getInvMass(), 0)):
			sep1 = coll["oneBody"].separateVector(coll)
			relSpeed1 = coll["oneBody"].relativeSpeed(coll["twoBody"])
			oneImpulse = coll["oneBody"].resolutionImpulse(coll["twoBody"], restitution, relSpeed1, sep1)
			coll["oneBody"].applyImpulse(oneImpulse*coll["oneBody"].getInvMass())
			oneFriction = coll["oneBody"].frictionImpulse(coll["twoBody"], sep1, oneImpulse.size())
			coll["oneBody"].applyImpulse(oneFriction*coll["oneBody"].getInvMass())
			coll["oneBody"].positionalCorrection(coll["twoBody"], sep1)
		#optimisation : ne pas résoudre les collisions pour les objets statiques
		if(not floatCmp(coll["twoBody"].getInvMass(), 0)):
			sep2 = coll["twoBody"].separateVector(coll)
			relSpeed2 = coll["twoBody"].relativeSpeed(coll["oneBody"])
			twoImpulse = coll["twoBody"].resolutionImpulse(coll["oneBody"], restitution, relSpeed2, sep2)
			coll["twoBody"].applyImpulse(twoImpulse*coll["twoBody"].getInvMass())
			twoFriction = coll["twoBody"].frictionImpulse(coll["oneBody"], sep2, twoImpulse.size())
			coll["twoBody"].applyImpulse(twoFriction*coll["twoBody"].getInvMass())
			coll["twoBody"].positionalCorrection(coll["oneBody"], sep2)
		#version avant optimisation
		# sep1 = coll["oneBody"].separateVector(coll)
		# sep2 = coll["twoBody"].separateVector(coll)
		# relSpeed1 = coll["oneBody"].relativeSpeed(coll["twoBody"])
		# relSpeed2 = coll["twoBody"].relativeSpeed(coll["oneBody"])
		# restitution = coll["oneBody"].minRestitution(coll["twoBody"])
		# oneImpulse = coll["oneBody"].resolutionImpulse(coll["twoBody"], restitution, relSpeed1, sep1)
		# twoImpulse = coll["twoBody"].resolutionImpulse(coll["oneBody"], restitution, relSpeed2, sep2)
		# coll["oneBody"].applyImpulse(oneImpulse*coll["oneBody"].getInvMass())
		# coll["twoBody"].applyImpulse(twoImpulse*coll["twoBody"].getInvMass())
		# oneFriction = coll["oneBody"].frictionImpulse(coll["twoBody"], sep1, oneImpulse.size())
		# twoFriction = coll["twoBody"].frictionImpulse(coll["oneBody"], sep2, twoImpulse.size())
		# coll["oneBody"].applyImpulse(oneFriction*coll["oneBody"].getInvMass())
		# coll["twoBody"].applyImpulse(twoFriction*coll["twoBody"].getInvMass())
		# coll["oneBody"].positionalCorrection(coll["twoBody"], sep1)
		# coll["twoBody"].positionalCorrection(coll["oneBody"], sep2)

def updatePhysics(dt, args, postManifolds = None, postSolve = None, gravity = None):
	colls = []
	if(postManifolds is None):
		postManifolds = lambda x: None
	if(postSolve is None):
		postSolve = lambda x: None
	if(gravity is None):
		gravity = Vec2(0, +0.9)
	for b1 in args:
		for b2 in args:
			if((not b1 is b2) and (b1.preCollide(b2))):
				mani = b1.collide(b2)
				if(not mani is None):
					colls.append(mani)
	colls = cullPairs(colls)
	postManifolds(colls)
	resolveCollisions(colls)
	for b in args:
	#application de la gravitée
		b.addForce(gravity)
		b.integrate(dt)
		b.zeroForce()