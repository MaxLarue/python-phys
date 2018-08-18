import time
import pprint

class bench:
	def __init__(self):
		self.__func = {}

	def getFuncEntry(self):
		return {"timeCalled":0, "avgTime":0, "times":[], "slowest":0, "fastest":0, "total time":0}

	def called(self, funcName):
		if(not funcName in self.__func.keys()):
			self.__func[funcName] = self.getFuncEntry()
		self.__func[funcName]["timeCalled"] += 1

	def executed(self, funcName, timeExec):
		self.__func[funcName]["times"].append(timeExec)

	def compute(self):
		for func in self.__func.keys():
			minTime = 99999999999999999999999999999999999
			maxTime = 0
			accumulator = 0
			for t in self.__func[func]["times"]:
				minTime = min(t, minTime)
				maxTime = max(t, maxTime)
				accumulator += t
			self.__func[func]["avgTime"] = accumulator/self.__func[func]["timeCalled"]
			self.__func[func]["slowest"] = maxTime
			self.__func[func]["fastest"] = minTime
			self.__func[func]["total time"] = accumulator

	def show(self):
		newDic = {}
		for f in self.__func.keys():
			newEntry = {}
			for f2 in self.__func[f].keys():
				if(f2 != "times"):
					newEntry[f2] = self.__func[f][f2]
			newDic[f] = newEntry
		pp = pprint.PrettyPrinter(indent = 4)
		print()
		pp.pprint(newDic)
		print()



BENCH = bench()

def timeit(method):

	def timed(*args, **kw):
		BENCH.called(repr(method))
		ts = time.time()*1000
		result = method(*args, **kw)
		te = time.time()*1000
		BENCH.executed(repr(method), te-ts)
		return result

	return timed