# -*- coding: utf-8 -*-
from collections import OrderedDict
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
            self.matrixDict[x]=self.matrix[x]
        self.solution = list()            # List with final solution
        for x in range(subsectors):
            self.solution.append(0)
        self.covered = list()    # Meaning each position is covered by X subsec
        for x in range(sectors):
            self.covered.append(0)
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.subsCoversOrdered = self.calcSubsectorsCoverDict()  # covers ordered
        self.solCost=0

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
        delete=[]
        for x in self.matrixDict.keys():
            if(self.matrixDict[x][subsector] == 1):
                delete.append(x)
        for x in delete:
            self.matrixDict.pop(x,None)
        self.subsCoversList = self.calcSubsectorsCover()


    """

    """
    def randomizedGreedy(self):
        auxMatrixDict = copy.deepcopy(self.matrixDict)
        while len(auxMatrixDict) != 0:
            rcl=[]
            NObjNoCov = len(auxMatrixDict)*0.7
            for x in range(self.subsCoversList):
                if(self.subsCoversList[x] >= NObjNoCov):
                    rcl.append(x)
            # Make RCL list
            # select random