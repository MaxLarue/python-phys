#	Test du module ADT
#
#
#
from ADT import *
import unittest
import random

class testVec2(unittest.TestCase):
	def test_constructor_no_arg(self):
		#le constructeur sans argument construit un Vec2 == (0.0, 0.0)
		testV = Vec2()
		self.assertEqual(testV.x(), 0.0)
		self.assertEqual(testV.y(), 0.0)

	def test_constructor_one_arg_tuple(self):
		testV = Vec2((3.0, 2.0))
		self.assertEqual(testV.x(), 3.0)
		self.assertEqual(testV.y(), 2.0)

	def test_constructor_one_arg_list(self):
		testV = Vec2([3.0, 2.0])
		self.assertEqual(testV.x(), 3.0)
		self.assertEqual(testV.y(), 2.0)

	def test_constructor_one_arg_str(self):
		testV = Vec2("Vec2(1.0, 2.0)")
		self.assertEqual(testV.x(), 1.0)
		self.assertEqual(testV.y(), 2.0)

	def test_constructor_two_arg(self):
		testV = Vec2(5, 7)
		self.assertEqual(testV.x(), 5.0)
		self.assertEqual(testV.y(), 7.0)		

	def test_constructor_exception(self):
		with self.assertRaises(Vec2Exception):
			test = Vec2("one", "two")
		with self.assertRaises(Vec2Exception):
			test = Vec2(("one", "two"))
		with self.assertRaises(Vec2Exception):
			test = Vec2("(1, 2)")
		with self.assertRaises(Vec2Exception):
			test = Vec2("one", 3)
		with self.assertRaises(Vec2Exception):
			test = Vec2(8)
		with self.assertRaises(Vec2Exception):
			test = Vec2("one")

	def test_get(self):
		self.assertEqual(Vec2(0.0, 2.0).get(), (0.0, 2.0))

	def test_x(self):
		self.assertEqual(Vec2(2.0, 3.0).x(), 2.0)

	def test_y(self):
		self.assertEqual(Vec2(2.0, 3.0).y(), 3.0)

	def test_getI(self):
		self.assertEqual(Vec2(0.0, 2.0).getI(), (0, 2))
		self.assertIsInstance(Vec2(0.0, 2.0).getI()[0], int)
		self.assertIsInstance(Vec2(0.0, 2.0).getI()[1], int)

	def test_xI(self):
		self.assertEqual(Vec2(0.0, 2.0).xI(), 0)
		self.assertIsInstance(Vec2(0.0, 2.0).xI(), int)

	def test_yI(self):
		self.assertEqual(Vec2(0.0, 2.0).yI(), 2)
		self.assertIsInstance(Vec2(0.0, 2.0).yI(), int)

	def test_getCopy(self):
		one = Vec2(5, 6)
		two = one.getCopy()
		self.assertEqual(one.x(), two.x())
		self.assertEqual(one.y(), two.y())

	def test_eq(self):
		self.assertEqual(Vec2(5.0, 6.0), Vec2((5, 6)))

	def test_add(self):
		self.assertEqual(Vec2(1.0, 5.0)+Vec2(5.0, 1.0), Vec2(3, 3)+Vec2(3, 3))

	def test_add_raise(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2(5, 6)+3

	def test_sub(self):
		self.assertEqual(Vec2(), Vec2(3, 3) - Vec2(3.0, 3.0).getCopy())

	def test_sub_raise(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2(8, 9) - 4

	def test_div(self):
		self.assertEqual(Vec2(6, 6)/2, Vec2(3, 3)/1)

	def test_div_raise_div_zero(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2(3, 3)/0

	def test_div_raise(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2(3, 3)/Vec2()

	def test_mul(self):
		self.assertEqual(Vec2(3, 3)*2, Vec2(6, 6))

	def test_mul_raise(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2(6, 6)*Vec2()

	def test_scalar(self):
		self.assertEqual(Vec2(6, 6).scalar(Vec2(9, 8)), 102)

	def test_scalar_raise(self):
		with self.assertRaises(Vec2Exception):
			x = Vec2().scalar(1)

	def test_unit(self):
		self.assertTrue(floatCmp(Vec2(5, 6).unit().size(), 1.0))

	def test_size(self):
		self.assertTrue(floatCmp(Vec2(3, 4).size(), 5))

	def test_sqSize(self):
		self.assertTrue(floatCmp(Vec2(3, 4).sqSize(), 25))



class testPQueue(unittest.TestCase):
	def test_construct(self):
		q = PQueue()
		self.assertEqual(q.size(), 0)

	def test_push_pop(self):
		q = PQueue()
		q.push(4, 4)
		q.push(3, 3)
		q.push(5, 5)
		self.assertEqual(q.pop(), (5, 5))
		self.assertEqual(q.pop(), (4, 4))
		q.push(20, 1)
		self.assertEqual(q.pop(), (20, 1))
		while(not q.empty()):
			q.pop()
		l = list(range(90))
		random.shuffle(l)
		for i in l:
			q.push(i, 1)
		self.assertEqual(q.pop(), (89, 1))
		l = list(reversed(range(89)))
		for i in l:
			poped = q.pop()
			self.assertEqual(poped, (i, 1))

class testGraph(unittest.TestCase):
	def test_build(self):
		g = Graph()
		self.assertEqual(g.size(), 0)
		v = Vertex(1)
		self.assertEqual(len(v.getConnections()), 0)
		v2 = Vertex(2)
		g.addVertex(v)
		g.addVertex(v2)
		g.addEdge(1, 2, 50)
		self.assertTrue(v.isNeighbor(v2.getKey()))
		self.assertTrue(v2.isNeighbor(v.getKey()))

	def test_getVertex(self):
		l = [(i, Vertex(i)) for i in range(5)]
		g = Graph()
		for i in range(5):
			g.addVertex(l[i][1])
		for i in range(5):
			self.assertIs(g.getVertex(l[i][0]), l[i][1])

	def test_getVerticesKeys(self):
		l = [(i, Vertex(i)) for i in range(5)]
		g = Graph()
		for i in range(5):
			g.addVertex(l[i][1])
		self.assertEqual(list(g.getVerticesKeys()), [i for i in range(5)])

	def test_is_in(self):
		l = [(i, Vertex(i)) for i in range(5)]
		g = Graph()
		for i in range(5):
			g.addVertex(l[i][1])
		for i in range(10):
			if(i < 5):
				self.assertTrue(g.isIn(i))
			else:
				self.assertFalse(g.isIn(i))

	def test_removeVertex(self):
		g = Graph()
		g.addVertex(Vertex(6))
		g.addVertex(Vertex(7))
		g.removeVertex(7)
		self.assertEqual(g.size(), 1)
		self.assertFalse(g.isIn(7))

	def test_djikstra_simple(self):
		"""
		A->B->C->D->E->
		 1  2  3  1  2

		de a vers d meilleur chemin : A-E-D
		"""
		g = Graph()
		for l in ["A", "B", "C", "D", "E"]:
			g.addVertex(Vertex(l))
		g.addEdge("A", "B", 1)
		g.addEdge("B", "C", 2)
		g.addEdge("C", "D", 3)
		g.addEdge("D", "E", 1)
		g.addEdge("E", "A", 2)
		cameFrom = djikstra(g, "A", "D")
		path = buildPathFromDjikstra(cameFrom, "A", "D")
		self.assertEqual(path, ["A", "E", "D"])

	def test_djikstra_complicate(self):
		"""
			A---------4-----------B---------2---------E
			|					 |					 |
			|					 |0                  |
			| 3             2    |                   |
			|--------C-----------F                   |6
					 |                               |
					 |4                              |
					 |                               G
					 D----------------8---------------

			de a vers G meilleur chemin : [A, B, E, G]

			de F vers A : [F, B, A]

		"""
		g = Graph()
		g.addVertex(Vertex("A"))
		g.addVertex(Vertex("B"))
		g.addVertex(Vertex("C"))
		g.addVertex(Vertex("D"))
		g.addVertex(Vertex("E"))
		g.addVertex(Vertex("F"))
		g.addVertex(Vertex("G"))
		g.addEdge("A", "B", 4)
		g.addEdge("A", "C", 3)
		g.addEdge("B", "F", 0)
		g.addEdge("B", "E", 2)
		g.addEdge("F", "C", 2)
		g.addEdge("C", "D", 4)
		g.addEdge("G", "D", 8)
		g.addEdge("G", "E", 6)
		cameFrom = djikstra(g, "A", "G")
		path = buildPathFromDjikstra(cameFrom, "A", "G")
		self.assertEqual(path, ["A", "B", "E", "G"])
		cameFrom = djikstra(g, "F", "A")
		path = buildPathFromDjikstra(cameFrom, "F", "A")
		self.assertEqual(path, ["F", "B", "A"])



class test_Ordered_List(unittest.TestCase):
	def test_Create(self):
		t = OrderedList()
		self.assertEqual(len(t), 0)
		t = OrderedList([1, 2, 3])
		self.assertEqual(len(t), 3)

	def test_add(self):
		t = OrderedList()
		t.add(1)
		self.assertEqual(len(t), 1)
		self.assertTrue(t.isIn(1))

	def test_remove(self):
		t = OrderedList([4, 1, 2, 3])
		t.remove(1)
		self.assertEqual(len(t), 3)
		t.removeAt(0)
		self.assertEqual(len(t), 2)

	def test_ordered(self):
		ok = True
		t = OrderedList([1, 8, 6, 4, 9, 7, 3, 0, 78, 5, 47, 12])
		prev = -1
		for i in t:
			ok = ok and i >= prev
			prev = i
		self.assertTrue(ok)

	def test_ordered_two(self):
		l = []
		for i in range(22):
			l.append(random.randrange(188))
		ok = True
		t = OrderedList(l)
		prev = -1
		for i in t:
			ok = ok and i >= prev
			prev = i
		print(t)
		self.assertTrue(ok)

	def test_len(self):
		t = OrderedList([1, 4, 3])
		self.assertEqual(len(t), 3)

	def test_isIn(self):
		t = OrderedList([4, 1, 2, 3])
		self.assertTrue(t.isIn(1))
		self.assertTrue(t.isIn(2))
		self.assertTrue(t.isIn(3))