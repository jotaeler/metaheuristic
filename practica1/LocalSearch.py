# -*- coding: utf-8 -*-
from collections import OrderedDict
import random
import copy


class LocalSearch:

    def __init__(self, costs, matrix, sectors, subsectors, initialSolution, initialSolCost, covered, seed, limit):
        random.seed(seed)
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
        self.limit=limit

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
                print("Coste de la solucion despues de borrar el sector"+str(x)+"="+str(cost))
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
            elif self.neihSubsCoversList[x] == self.neihSubsCoversList[biggest] and biggest != x:
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
        #print("Ratios en select "+str(self.neihRatios))
        reverseIndex = -2
        index = 0
        candidates.append(fulllist[-1])  # key of biggest ratio
        ret = 0
        #print("fulllist="+str(fulllist))
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
        elif len(candidates) == 1:
            ret=candidates[0]
        else:
            ret=None
            print("SELECT no sector can cover")
        return ret

    """
    Generate new neihtbourg
    Return list [solution, cost, Have solution]
    """
    def genNeihtbourg(self,arg):
        solution = arg['solution']
        subsector = arg['subsector']
        rand=0
        neihtbourg = {}
        neihtbourg['firstRand'] = arg['firstRand']
        candidatesToRand=[]
        stop = False
        firstRand=False
        for x in range(len(solution)):
            if(solution[x] == 1):
                candidatesToRand.append(x)
        if subsector == -1:
            rand = random.randint(0,len(candidatesToRand)-1)
            neihtbourg['firstRand'] = candidatesToRand[rand]
            subsector = candidatesToRand[rand]
            firstRand=True
        else:
            if subsector+1 == len(candidatesToRand):
                subsector=0
            else:
                print("subsector="+str(subsector)+" len candidates="+str(len(candidatesToRand)))
                rand = subsector+1
                subsector = candidatesToRand[subsector+1]
        if subsector == arg['firstRand'] and firstRand == False:
            stop = True
            print("E(actual solution) complete")
        else:
            neihtbourg['solution'] = copy.deepcopy(solution)
            #delete rows covered
            delete=[]
            print("antes de poner a 0="+str(neihtbourg['solution'][subsector]))
            neihtbourg['solution'][subsector] = 0
            for x in range(self.subsectors):
                if neihtbourg['solution'][x] == 1:
                    for y in self.neihtbourgMatrix.keys():
                        if(self.neihtbourgMatrix[y][x] == 1):
                            delete.append(y)
                    for y in delete:
                        self.neihtbourgMatrix.pop(y,None)
            cost = self.bestSolutionCost
            cost -= self.costs[subsector]
            self.neihSubsCoversList[subsector] = 0
            self.neihRatios = self.getRatios()
            self.setSectorsAtUnCovered(subsector)
            print("Coste despues de poner a 0 el sector"+str(cost)+" tamaño de la matriz ="+str(len(self.neihtbourgMatrix)))
            while not(stop) and len(self.neihtbourgMatrix) != 0:
                # Select candidates subsector for solution
                nextS=self.select()
                if nextS == None :
                    stop=True
                    print("no sector can cover")
                else:
                    print("next sector for solution"+str(nextS))
                    neihtbourg['solution'][nextS] = 1
                    #print("matrix dict"+str(self.neihtbourgMatrix)+" STOP="+str(stop)+" otra condicion="+str(len(self.neihtbourgMatrix) != 0))
                    cost += self.costs[nextS]
                    self.recalculateMatrix(nextS)
                    print("Coste despues de añadir el sector="+str(cost))
            delete = self.delete(neihtbourg['solution'],cost)
            neihtbourg['solution'] = delete['solution']
            neihtbourg['subsector'] = rand
            neihtbourg['cost'] = delete['cost']
        neihtbourg['continue'] = not(stop)
        return neihtbourg
    """
    Reinitialize data structures or update it
    """
    def updateMemory(self, reinitialize):
        self.neihtbourgMatrix = copy.deepcopy(self.matrixDict)
        self.neihSubsCoversList = copy.deepcopy(self.subsCoversList)
        for x in range(len(self.bestSolution)):
            if self.bestSolution[x] == 1:
                self.neihSubsCoversList[x] = 0
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
            neihtbourg = self.genNeihtbourg(neihtbourg)
            if neihtbourg['continue']:
                print("Coste del vecino="+str(neihtbourg["cost"]))
                if(neihtbourg["cost"]<self.bestSolutionCost):
                    neihtbourg['subsector'] = -1
                    neihtbourg['firstRand'] = -1
                    self.bestSolution = copy.deepcopy(neihtbourg['solution'])
                    self.bestSolutionCost=neihtbourg["cost"]
                    neihtbourg['solution'] = self.bestSolution
                    #neihtbourg['cost'] = self.bestSolutionCost
                    self.updateMemory(False)
                    print("SOLUCION ="+str(neihtbourg["solution"]))
                else:
                    self.updateMemory(True)
                iterations += 1
                print("iterations BL="+str(iterations))
                if iterations == self.limit:
                    stop=True
            else:
                stop = True
