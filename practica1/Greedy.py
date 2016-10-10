class Greedy:
	"""
	Sectors and subsectors starts at 0 and goes to X-1
	When calling a function be sure to use number 0 for sector 1
	"""
	def __init__(self, costs, matrix, sectors, subsectors):
		self.costs = costs			# List with cost of each subsector
		self.matrix = matrix  # Bin matrix meaning wich subsctr covers each sec
		self.sectors = sectors		# Int, number of sectors
		self.subsectors = subsectors	# Int, number of subsectors
		self.solution = list()			# List with final solution
		self.covered = list()	# Meaning each position is covered by X subsec
		self.ratios = self.getRatios()		# Dict with subsector (key) ratios (value)
		self.totalCosts= self.calcTotalCosts() # List with total cost of each subsector
		self.subsCoversList=self.calcSubsectorsCover() #covers
		self.subsCoversOrdered=self.calcSubsectorsCoverDict() #covers ordered
	"""
	Returns how many sectors (cities) are covered by one
	subsector a.k.a. hospital
	"""
	def getSubsectorCover(self, subsector):
		total=0
		for x in range(0,self.sectors-1):	# -1 because list start at 0
			total=total+self.matrix[x][subsector]
		return total
	
	"""
	Return an ordered dictionary where key is subsector and value number of
	sectors covered by it
	"""
	def calcSubsectorsCoverDict(self):
		ret={}
		for x in range(0,self.subsectors-1):	# -1 because list start at 0
			ret[x]=self.subsCoversList[x]
		return sorted(ret.items(), key=lambda t: t[1])		# ordered
		
	"""
	Return a list with number of sectors covered by subsector (list position)
	"""
	def calcSubsectorsCover(self):
		ret=[]
		for x in range(0,self.subsectors-1):	# -1 because list start at 0
			total=0
			for y in range(0,self.sectors-1):	# -1 because list start at 0
				total=total+self.matrix[y][x]	# moving through sectors first
			ret[x]=total
		return ret
		
	"""
	Return list with total costs
	"""
	def calcTotalCosts(self):
		ret=[]
		for x in range(0, self.subsectors-1):
			ret[x]=self.subsCoversList*self.costs[x]
		return ret
		
	"""
	Returns subsector ratio
	"""
	def getRatios(self):
		ret={}
		for x in range(len(self.costs)):
			ret[x]=(self.subsCoversList[x]/self.totalCosts[x])
		return sorted(ret.items(), key=lambda t: t[1])		# ordered
	
	"""
	Auxiliar function for Delete, return ordered dict with covers only for
	selected subsectors
	"""
	def getSelectedCovers(self):
		for x in range(0, self.subsectors):
			if(self.solution[x]==1):
				
	"""
	Delete unnecessary subsectors a.k.a. hospitals
	"""
	def delete(self, coverage):
		pass

	"""
	Returns the next subsector to be taken
	"""
	def select(self):
		for x in range(0, self.subsectors-1):
	
	"""
	Returns the solution
	"""
	def start(self):
		pass
