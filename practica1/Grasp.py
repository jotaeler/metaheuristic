# -*- coding: utf-8 -*-
from collections import OrderedDict
from LocalSearch import LocalSearch
import random
import copy


"""
Greedy Randomized Adaptive Search Procedures
"""


class Grasp:

    def __init__(self, costs, matrix, sectors, subsectors, seed, limit):
        random.seed(seed)
        self.costs = costs            # List with cost of each subsector
        self.sectors = sectors        # Int, number of sectors
        self.subsectors = subsectors    # Int, number of subsectors
        self.matrix = matrix  # Bin matrix meaning wich subsctr covers each sec
        self.matrixDict={}
        for x in range(self.sectors):
            self.matrixDict[x] = self.matrix[x]
        self.neihMatrixDict = copy.deepcopy(self.matrixDict)
        self.solution = list()            # List with final solution
        for x in range(subsectors):
            self.solution.append(0)
        self.bestSolution = [x*0 for x in range(self.subsectors)]
        self.solCost = 0
        self.bestSolutionCost = 0
        self.covered = list()    # Meaning each position is covered by X subsec
        for x in range(sectors):
            self.covered.append(0)
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.subsCoversOrdered = self.calcSubsectorsCoverDict()  # covers ordered
        self.limit = limit


    """
    Return an ordered dictionary where key is subsector and value number of
    sectors covered by it
    """
    def calcSubsectorsCoverDict(self):
        ret = {}
        for x in range(0, self.subsectors):  # -1 because list start at 0
            ret[x] = self.subsCoversList[x]
        return sorted(ret.items(), key=lambda t: t[1])  # ordered

    """
    Return a list with number of sectors covered by subsectors (list position)
    """
    def calcSubsectorsCover(self):
        ret = []
        for x in range(self.subsectors):
            total = 0
            for y in self.matrixDict.keys():
                total = total + self.matrixDict[y][x]  # moving through sectors first
            ret.append(total)
        return ret

    """
    Return a list with number of sectors covered by subsectors (list position)
    """
    def calcNObjNoCov(self):
        ret = 0
        for x in range(self.subsectors):
            total = 0
            for y in self.neihMatrixDict.keys():
                if self.neihMatrixDict[y][x] == 0:
                    total += 1
            if total > ret:
                ret = total
        return ret

    """
    Aux function for Delete, return ordered dict with covers only for
    selected subsectors
    """
    def getSelectedCovers(self):
        ret = OrderedDict()
        for x in range(self.subsectors):
            if self.solution[x] == 1:
                ret[x] = self.subsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1], reverse=True))

    """
    Delete unnecessary subsectors a.k.a. hospitals
    """
    def delete(self):
        subsectors = self.getSelectedCovers()
        for x in subsectors.keys():
            # subs = subsectors.popitem(True)  #return the last item (biggest cover value)
            stop = False
            delete = False
            y = 0
            while not stop :
                if self.matrix[y][x] == 1 :
                    if self.covered[y]-1 == 0 :
                        stop = True
                y += 1
                if y == self.sectors-1 :
                    delete = True
                    stop = True
            if delete :
                self.setSectorsAtUnCovered(x)
                self.solution[x] = 0  # Delete item from solution

    """
    Given one subsector set each sectors covered by it as UNcovered
    """
    def setSectorsAtUnCovered(self, subsector):
        for x in range(self.sectors):
            if(self.matrix[x][subsector] == 1):
                self.covered[x] -= 1
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
        delete = []
        for x in self.neihMatrixDict.keys():
            if(self.neihMatrixDict[x][subsector] == 1):
                delete.append(x)
        for x in delete:
            self.neihMatrixDict.pop(x,None)

    """
    Calc Solution Cost
    """
    def solutionCost(self,solution):
        total = 0
        for x in range(self.subsectors):
            if (solution[x] == 1):
                total += self.costs[x]
        return total

    """
    Randomize Greedy through RCL list
    """
    def randomizedGreedy(self):
        while len(self.neihMatrixDict) != 0:
            rcl=[]
            MaxObjCov = self.calcNObjNoCov()*0.7
            for x in range(self.subsectors):
                if self.subsCoversList[x] >= MaxObjCov and self.subsCoversList[x] != 0:
                    rcl.append(x)
            rand = random.randint(0, len(rcl)-1)
            candidate = rcl[rand]
            self.solution[candidate] = 1
            self.recalculateMatrix(candidate)
        self.delete()
        return self.solution

    """
    Copy data structures
    """
    def updateMemory(self):
        self.neihMatrixDict = copy.deepcopy(self.matrixDict)
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        for x in range(self.subsectors):
            self.solution[x] = 0
        for x in range(self.sectors):
            self.covered[x] = 0

    """
    Start Grasp Algorithm
    """
    def start(self):
        iterations = 0
        while iterations < self.limit:
            self.solution = self.randomizedGreedy()
            cost = self.solutionCost(self.solution)
            print("Coste de la solucion random="+str(cost))
            bl = LocalSearch(self.costs, self.matrix, self.sectors, self.subsectors, self.solution, cost, self.covered, "1234", 400)
            bl.start()
            if bl.bestSolutionCost < self.bestSolutionCost:
                print("Mejor solucion encontrada con coste ="+str(bl.bestSolutionCost))
                self.bestSolution = bl.bestSolution
                self.bestSolutionCost = bl.bestSolutionCost
            iterations += (bl.iterations + 1)
            self.updateMemory()
            print("Iterations ="+str(iterations))
        print("Finalizado GRASP con coste="+str(self.bestSolutionCost))