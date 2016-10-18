# -*- coding: utf-8 -*-
from collections import OrderedDict
import random
import copy
random.seed("1234")

class LocalSearch:

    def __init__(self, costs, matrix, sectors, subsectors, initialSolution, initialSolCost, covered):
        self.costs = costs            # List with cost of each subsector
        self.sectors = sectors        # Int, number of sectors
        self.subsectors = subsectors    # Int, number of subsectors
        self.matrix = matrix  # Bin matrix meaning wich subsctr covers each sec
        self.matrixDict={}
        for x in range(self.sectors):
            self.matrixDict[x]=self.matrix[x]
        self.neihtbourgMatrix = copy.deepcopy(self.matrixDict)
        self.bestSolution = initialSolution       # List with final solution
        self.bestSolutionCost = initialSolCost
        self.covered = covered    # Meaning each position is covered by X subsec
        self.neihCovered = copy.deepcopy(self.covered)
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.neihSubsCoversList = copy.deepcopy(self.subsCoversList)
        self.ratios = self.getRatios()        # Dict with subsector (key) ratios (value)
        self.neihRatios = copy.deepcopy(self.ratios)
        self.subsCoversOrdered = self.calcSubsectorsCoverDict() #covers ordered
        self.neihSubsCoversOrdered = copy.deepcopy(self.subsCoversOrdered)

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
            for y in self.matrixDict.keys():
                total = total+self.matrixDict[y][x]    # moving through sectors first
            ret.append(total)
        return ret

    """
    Return a list with number of sectors covered by subsectors (list position)
    """
    def calcSubsectorsCoverNeihtbourg(self):
        ret = []
        for x in range(self.subsectors):
            total = 0
            for y in self.neihtbourgMatrix.keys():
                total = total+self.neihtbourgMatrix[y][x]    # moving through sectors first
            ret.append(total)
        return ret

    """
    Returns subsector ratio
    """
    def getRatios(self):
        ret = OrderedDict()
        for x in range(len(self.costs)):
            ret[x] = (self.neihSubsCoversList[x]/self.costs[x])
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1]))   # ordered

    """
    Aux function for Delete, return ordered dict with covers only for
    selected subsectors
    """
    def getSelectedCovers(self,solution):
        ret = OrderedDict()
        for x in range(self.subsectors):
            if(solution[x] == 1):
                ret[x] = self.neihSubsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1], reverse=True))

    """
    Delete unnecessary subsectors a.k.a. hospitals
    """
    def delete(self, solution, cost):
        subsectors = self.getSelectedCovers(solution)
        for x in subsectors.keys():
            #subs = subsectors.popitem(True)  #return the last item (biggest cover value)
            stop = False
            delete = False
            y = 0
            while not(stop):
                if(self.matrix[y][x] == 1):
                    if(self.neihCovered[y]-1 == 0):
                        stop = True
                y += 1
                if(y == self.sectors-1):
                    delete = True
                    stop = True
            if(delete):
                self.setSectorsAtUnCovered(x)
                solution[x] = 0  # Delete item from solution
                cost -= self.costs[x]
        ret = {'solution':solution, 'cost':cost}
        return ret

    """
    Given candidates, return wich one has
    biggest cover value or random if equal
    """
    def biggestCover(self, candidates):
        biggest = candidates[0]
        randomCandidates = []
        for x in candidates: # x isn't index, x is subsector'
            if self.neihSubsCoversList[x] > self.neihSubsCoversList[biggest]:
                biggest = x
            elif self.neihSubsCoversList[x] == self.neihSubsCoversList[biggest] & biggest != x:
                randomCandidates.append(x)
        if(len(randomCandidates) > 0):
            randCandidate = random.randint(0, len(randomCandidates)-1)
            biggest=randomCandidates[randCandidate]
        return biggest

    """
    Given one subsector set each sectors covered by it as UNcovered
    """
    def setSectorsAtUnCovered(self, subsector):
        for x in range(self.sectors):
            if(self.matrix[x][subsector] == 1):
                self.neihCovered[x] -= 1
    """
    Given one subsector set each sectors covered by it as covered
    """
    def setSectorsAtCovered(self, subsector):
        for x in range(self.sectors):
            if(self.matrix[x][subsector] == 1):
                self.neihCovered[x] += 1
    """
    Recalculate matrix after select a subsector
    """
    def recalculateMatrix(self, subsector):
        self.setSectorsAtCovered(subsector)
        self.neihSubsCoversList[subsector] = 0
        delete=[]
        for x in self.neihtbourgMatrix.keys():
            if(self.neihtbourgMatrix[x][subsector] == 1):
                delete.append(x)
        for x in delete:
            self.neihtbourgMatrix.pop(x,None)
        self.neihSubsCoversList = self.calcSubsectorsCoverNeihtbourg()
        self.neihRatios = self.getRatios()

    """
    Returns the next subsector to be taken
    """
    def select(self):
        stop = False
        candidates = []  # candidates to randomize
        fulllist = list(self.neihRatios.keys())  # all keys
        reverseIndex = -2
        index = 0
        candidates.append(fulllist[-1])  # key of biggest ratio
        ret = 0
        print("fulllist="+str(fulllist))
        while not(stop):
            if self.neihRatios[candidates[index]] == self.neihRatios[fulllist[reverseIndex]]:
                index += 1
                candidates.append(fulllist[reverseIndex])
                reverseIndex-=1
            else:
                stop = True
        if(len(candidates) > 1):
            print("candidates SELECT="+str(candidates))
            ret = self.biggestCover(candidates)
            self.recalculateMatrix(ret)
        elif len(candidates) == 1:
            ret=candidates[0]
            self.recalculateMatrix(ret)
        else:
            ret=None
        return ret

    """
    Generate new neihtbourg
    Return list [solution, cost, Have solution]
    """
    def genNeihtbourg(self,solution, subsector):
        neihtbourg = {}
        candidatesToRand=[]
        stop = False
        firstRand=False
        for x in range(len(solution)):
            if(solution[x] == 1):
                candidatesToRand.append(x)
        if subsector == -1:
            subsector = random.randint(0,len(candidatesToRand)-1)
            neihtbourg['firstRand'] = subsector
            firstRand=True
        else:
            if subsector+1 == len(candidatesToRand):
                subsector=0
            else:
                subsector = subsector+1
        if subsector == neihtbourg['firstRand'] & firstRand == False:
            stop = True
            print("E(actual solution) complete")
        else:
            neihtbourg['solution'] = copy.deepcopy(solution)
            #delete rows covered
            delete=[]
            for x in range(self.subsectors):
                if neihtbourg['solution'][x] == 1:
                    for y in self.neihtbourgMatrix.keys():
                        if(self.neihtbourgMatrix[y][x] == 1):
                            delete.append(y)
                    for y in delete:
                        self.neihtbourgMatrix.pop(y,None)
            cost = self.bestSolutionCost
            print("candidates="+str(len(candidatesToRand)))
            print("subsector="+str(subsector))
            print("candidate to rand"+str(candidatesToRand[subsector]))
            cost -= self.costs[candidatesToRand[subsector]]
            self.neihSubsCoversList[candidatesToRand[subsector]] = 0
            self.neihRatios = self.getRatios()
            self.setSectorsAtUnCovered(candidatesToRand[subsector])

            while not(stop) & len(self.neihtbourgMatrix) != 0:
                # Select candidates subsector for solution
                nextS=self.select()
                if nextS == None :
                    stop=True
                    print("no sector can cover")
                else:
                    print("next sector for solution"+str(nextS))
                    solution[nextS] = 1
                    cost += self.costs[nextS]
            delete = self.delete()
            neihtbourg['solution'] = delete['solution']
            neihtbourg['subsector'] = subsector
            neihtbourg['cost'] = delete['cost']
        neihtbourg['continue'] = not(stop)
        return neihtbourg
    """
    Reinitialize data structures or update it
    """
    def updateMemory(self, reinitialize):
        self.neihtbourgMatrix = copy.deepcopy(self.matrixDict)
        self.neihSubsCoversList = copy.deepcopy(self.subsCoversList)
        if reinitialize:
            self.neihCovered = copy.deepcopy(self.covered)
        else:
            self.covered = copy.deepcopy(self.neihCovered)

    """
    Returns the solution
    """
    def start(self):
        for x in range(len(self.bestSolution)):
            if self.bestSolution[x] == 1:
                self.neihSubsCoversList[x] = 0
        iterations = 0
        stop = False
        # Solution, cost, sector changed (only from "ones"), Boolean for continue loop or not
        neihtbourg= {'solution':self.bestSolution, 'cost':self.bestSolutionCost,'subsector': -1,'continue':True, 'firstRand':-1}
        while not(stop):
            neihtbourg= self.genNeihtbourg(neihtbourg['solution'],neihtbourg['subsector'])
            if neihtbourg['continue']:
                if(neihtbourg["cost"]<self.bestSolutionCost):
                    neihtbourg['subsector'] = -1
                    self.bestSolution = copy.deepcopy(neihtbourg['solution'])
                    self.bestSolutionCost=neihtbourg["cost"]
                    self.updateMemory()
                iterations += 1
                if iterations == 10000:
                    stop=True
            else:
                stop = True
        print("iterations BL="+str(iterations))