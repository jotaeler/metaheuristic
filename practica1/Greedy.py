from collections import OrderedDict
import random
random.seed("1234")

class Greedy:

    """
    Sectors and subsectors starts at 0 and goes to X-1
    When calling a function be sure to use number 0 for sector 1
    """
    def __init__(self, costs, matrix, sectors, subsectors):
        self.costs = costs            # List with cost of each subsector
        self.sectors = sectors        # Int, number of sectors
        self.subsectors = subsectors    # Int, number of subsectors
        self.matrix = matrix  # Bin matrix meaning wich subsctr covers each sec
        self.matrixDict={}
        for x in range(self.sectors):
            self.matrixDict[x]=self.matrix[x]
        self.solution = list()            # List with final solution
        for x in range(subsectors):
            self.solution.append(0)
        self.covered = list()    # Meaning each position is covered by X subsec
        for x in range(sectors):
            self.covered.append(0)
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.totalCosts = self.calcTotalCosts() # List with total cost of each subsector
        self.ratios = self.getRatios()        # Dict with subsector (key) ratios (value)
        self.subsCoversOrdered = self.calcSubsectorsCoverDict() #covers ordered

    """
    Return an ordered dictionary where key is subsector and value number of
    sectors covered by it
    """
    def calcSubsectorsCoverDict(self):
        ret = {}
        for x in range(0, self.subsectors):    # -1 because list start at 0
            ret[x] = self.subsCoversList[x]
        return sorted(ret.items(), key=lambda t: t[1])        # ordered

    """
    Return a list with number of sectors covered by subsectors (list position)
    """
    def calcSubsectorsCover(self):
        ret = []
        for x in range(self.subsectors):
            total = 0
            for y in range(len(self.matrixDict)):
                total = total+self.matrixDict[y][x]    # moving through sectors first
            ret.append(total)
        return ret

    """
    Return list with total costs
    """
    def calcTotalCosts(self):
        ret = []
        for x in range(self.subsectors):
            ret.append(self.subsCoversList[x]*self.costs[x])
        return ret

    """
    Returns subsector ratio
    """
    def getRatios(self):
        ret = OrderedDict()
        for x in range(len(self.costs)):
            ret[x] = (self.subsCoversList[x]/self.totalCosts[x])
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1]))   # ordered

    """
    Aux function for Delete, return ordered dict with covers only for
    selected subsectors
    """
    def getSelectedCovers(self):
        ret = OrderedDict()
        for x in range(0, self.subsectors):
            if(self.solution[x] == 1):
                ret[x] = self.subsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1]))

    """
    Delete unnecessary subsectors a.k.a. hospitals
    """
    def delete(self):
        subsectors = self.getSelectedCovers()
        for x in range(self.subsectors):
            subs = subsectors.popitem(True)  #return the last item (biggest cover value)
            stop = False
            delete = False
            y = 0
            while not(stop):
                if(self.matrix[y][subs[0]] == 1):
                    if(self.covered[y]-1 == 0):
                        stop = True
                y += 1
                if(y == self.sectors-1):
                    delete = True
                    stop = True
            if(delete):
                self.solution[subs[0]] = 0  # Delete item from solution

    """
	Given candidates, return wich one has
	biggest cover value or random if equal
    """
    def biggestCover(self, candidates):
        biggest = candidates[0]
        randomCandidates = []
        for x in candidates: # x isn't index, x is de subsector'
            if self.subsCoversList[x] > self.subsCoversList[biggest]:
                biggest = x
            elif self.subsCoversList[x] == self.subsCoversList[biggest] & x != 0:
                randomCandidates.append(self.subsCoversList[x])

        if(len(randomCandidates) > 0):
            biggest = random.randint(0, len(randomCandidates)-1)
        return biggest

    """
    Given one subsector set each sectors covered by it as covered
    """
    def setSectorsAtCovered(self, subsector):
        for x in range(self.sectors):
            if(self.matrix[x][subsector] == 1):
                self.covered[x] += 1
    """
    Recalculate matrix after select a subsector
    """
    def recalculateMatrix(self, subsector):
        self.setSectorsAtCovered(subsector)
        self.subsCoversList[subsector] = 0
        for x in range(self.sectors):
            if(self.matrixDic[x][subsector] == 1):
                self.matrixDic.pop(x,None)
        self.subsCoversList = self.calcSubsectorsCover()
        self.ratios = self.getRatios()

    """
    Returns the next subsector to be taken
    """
    def select(self):
        stop = False
        candidates = []  # candidates to randomize
        fulllist = list(self.ratios.keys())  # all keys
        #print(str("ratios keys="+str(fulllist)))
        reverseIndex = -2
        index = 0
        candidates.append(fulllist[-1])  # key of biggest ratio
        ret = 0
        while not(stop):
            if self.ratios[candidates[index]] == self.ratios[fulllist[reverseIndex]]:
                index += 1
                candidates.append(fulllist[reverseIndex])
                reverseIndex-=1
            else:
                stop = True
        if(len(candidates) > 1):
            ret = self.biggestCover(candidates)
        #we have candidate, remake ratios list and set 0 to covers on given subsector
        self.recalculateMatrix(ret)
        #print("candidato para esta iteracion="+str(ret)+" ratio para siguente iteracion="+str(self.ratios[ret]))
        return ret

    """
    Return if a solution is reached based on covered list
    """
    def solutionReached(self):
        ret = True
        for x in range(self.sectors):
            if(self.covered[x] == 0):
                ret = False
                break
        return ret
    """
    Returns the solution
    """
    def start(self):
        while not(len(self.matrixDict)!=0):
            self.solution[self.select()] = 1
            print(str(self.solution))
        self.delete()
