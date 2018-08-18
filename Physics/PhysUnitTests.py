import unittest
from body import *
import random
import tkinter as tk
import time


class test_shape(unittest.TestCase):
	def test_construct(self):
		t = Shape()
		self.assertEqual(t.nbOfPoints(), 0)
		t = Shape([(0, 0), (0, 0), (0, 0)])
		self.assertEqual(t.nbOfPoints(), 3)
		 

	def test_get_normals(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		norms = t.getNormals()
		waitedNorms = [Vec2(-1.0, 0.0), Vec2(0.0, 1.0), Vec2(1.0, 0.0), Vec2(0.0, -1.0)]
		self.assertEqual(len(norms), 4)
		ok = True
		for i in range(4):
			ok = ok and floatCmp(waitedNorms[i].x(), norms[i].x()) and floatCmp(waitedNorms[i].y(), norms[i].y())
		self.assertTrue(ok)

	def test_get_center(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		self.assertEqual(t.getCenter(), Vec2(15.0, 25.0))

	def test_get_radius(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		self.assertEqual(t.getRadius(), (15*15 + 25*25)**(1/2) )

	def test_get_trans_point(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		newP = t.getTransPoints(Vec2(1, 1))
		self.assertTrue(floatCmp(newP[2].y(), 1.0))

	def test_get_center_trans(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		newCenter = t.getCenterTrans(Vec2(1, 1))
		self.assertTrue( floatCmp(newCenter.x(), 16.0) and floatCmp(newCenter.y(), 26.0) )

	def test_get_area(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		self.assertTrue(floatCmp(t.getArea(), 50.0*30.0))
		t = Shape([(0.0, 0.0), (0.0, 30.0), (50.0, 0.0)])
		self.assertTrue(floatCmp(t.getArea(), 50.0*30.0/2))

	def test_SAT(self):
		t1 = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		t2 = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		mani = SAT(t1, t2, Vec2(0, 0), Vec2(500, 500))
		self.assertTrue(mani is None)
		pos1 = Vec2(0, 0)
		pos2 = Vec2(15, 15)
		# #pdb.set_trace()
		mani = SAT(t1, t2, pos1, pos2)
		self.assertTrue(not mani is None)
		pos2 = pos2 + Vec2(1, 0)*mani["magnitude"]
		mani = SAT(t1, t2, pos1, pos2)
		self.assertTrue(mani is None)

	def test_SAT_2(self):
		t1 = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		t2 = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		pos1 = Vec2(30, 30)
		pos2 = Vec2(50, 50)
		mani = SAT(t1, t2, pos1, pos2)
		self.assertTrue(not mani is None)
		mani2 = SAT(t1, t2, pos1, pos2+Vec2(1, 0)*mani["magnitude"])
		self.assertTrue(mani2 is None)

	def test_pre_collide(self):
		t = Shape([(0.0, 50.0), (30.0, 50.0), (30.0, 0.0), (0.0, 0.0)])
		self.assertTrue(preCollide(t, t, Vec2(), Vec2(15, 15)))
		self.assertFalse(preCollide(t, t, Vec2(), Vec2(100, 100)))
		self.assertTrue(preCollide(t, t, Vec2(), Vec2(31, 0)))
		#pre-collide retourne True mais pas le SAT
		self.assertTrue(SAT(t, t, Vec2(), Vec2(31, 0)) is None)

	def test_get_reg_polygon(self):
		p = getRegPolygon(25, 100, Vec2(0, 0))
		self.assertTrue(floatCmp(p.getRadius(), 100))

class testBody(unittest.TestCase):
	def test_build(self):
		b = Body(AABB(50, 50), "Rock")
		self.assertEqual(b.getPos(), Vec2(0, 0))
		self.assertTrue(floatCmp(b.getMass(), 1500))
		self.assertEqual(b.getDensity(), 0.6)
		self.assertEqual(b.getRestitution(), 0.1)
		b = Body(AABB(50, 50), "Static")

	def test_collide(self):
		b1 = Body(AABB(50, 50), "Rock")
		b2 = Body(Shape([Vec2(0, 0), Vec2(45, 45), Vec2(45, 0)]), "Rock")
		b1.teleport(Vec2(0, 25))
		mani = b1.collide(b2)
		self.assertTrue(not mani is None)
		#pdb.set_trace()
		b2.teleport(b2.separateVector(mani))
		mani = b1.collide(b2)
		self.assertTrue(mani is None)

	def test_collide2(self):
		b1 = Body(AABB(50, 50), "Rock")
		b2 = Body(getRegPolygon(8, 50), "Rock")
		b1.teleport(Vec2(0, 25))
		mani = b1.collide(b2)
		self.assertTrue(not mani is None)
		b2.teleport(b2.separateVector(mani))
		mani = b1.collide(b2)
		self.assertTrue(mani is None)

	def test_integrate(self):
		b = Body(AABB(50, 50), "Rock")
		b.addForce(Vec2(50, 50))
		b.integrate(1)
		self.assertEqual(b.getPos(), Vec2(0.03333333333333333333, 0.033333333333333333333))

