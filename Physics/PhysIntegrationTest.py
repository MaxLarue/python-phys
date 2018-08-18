import unittest
from body import *
import random
import tkinter as tk
import time



def addBody(event, bodyList):
	bodyList.append(Body(getRegPolygon(3, 30), "Metal"))
	bodyList[-1].teleport(Vec2(event.x-250, event.y-250))	

def genTk(dt):
	window = tk.Tk()
	c = tk.Canvas(window, width = 500, height = 500)
	c.pack()
	bodies = []
	#bords
	horizCenter = AABB(500, 30).getCenter()
	vertiCenter = AABB(30, 500).getCenter()
	bodies.append(Body(AABB(500, 30), "Static"))
	bodies[-1].teleport(Vec2(0, 230) - horizCenter)
	bodies.append(Body(AABB(500, 30), "Static"))
	bodies[-1].teleport(Vec2(0, -230) - horizCenter)
	bodies.append(Body(AABB(30, 500), "Static"))
	bodies[-1].teleport(Vec2(-230, 0) - vertiCenter)
	bodies.append(Body(AABB(30, 500), "Static"))
	bodies[-1].teleport(Vec2(230, 0) - vertiCenter)
	#objets
	# bodies.append(Body(AABB(50, 50), "Rock"))
	# bodies[-1].teleport(Vec2(0, -100))
	# bodies.append(Body(getRegPolygon(3, 50), "Wood"))
	# bodies.append(Body(getRegPolygon(5, 50), "Wood"))
	# bodies.append(Body(getRegPolygon(6, 50), "Rock"))
	# bodies.append(Body(getRegPolygon(7, 50), "Rock"))
	#
	bodies.append(Body(AABB(50, 50), "Rock"))
	bodies[-1].teleport(Vec2(0, -100))
	bodies.append(Body(getRegPolygon(4, 50), "Wood"))
	bodies.append(Body(getRegPolygon(4, 50), "Wood"))
	bodies.append(Body(getRegPolygon(4, 50), "Rock"))
	bodies.append(Body(getRegPolygon(4, 50), "Rock"))
	#
	window.after(dt, lambda: update(window, c, dt, bodies))
	window.bind("<Button-1>", lambda x: addBody(x, bodies))
	window.mainloop()

def update(TK, c, dt, bodies):
	for i in range(2):
		updatePhysics(dt, bodies)
	renderScene(TK, c, bodies)
	TK.after(dt, lambda: update(TK, c, dt, bodies))



def renderScene(TK, c, args):
	c.delete("all")
	colors = ["red", "blue", "green", "black"]
	for i in range(len(args)):
		b = args[i]
		color = colors[i%len(colors)]
		for s in [b.getShape()]:
			ps = s.getTransPoints(b.getPos())
			ps.append(ps[0])
			for start in range(len(ps) - 1):
				c.create_line(ps[start].x() + 250, 250 + ps[start].y(), ps[start+1].x() + 250, 250 + ps[start+1].y(), fill=color)

if(__name__ == "__main__"):
		fps = 100
		dt = int(1/fps*1000)
		genTk(dt)
