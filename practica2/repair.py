from Bio.GA import Organism
import copy
from collections import OrderedDict
import random

class Repair(object):

    def __init__(self, matrix, nSectors, nSubsectors, costs):
        random.seed("1234")
        self.matrix = matrix
        self.matrixDict = {}
        for x in range(self.sectors):
            self.matrixDict[x] = self.matrix[x]
        self.sectors = nSectors
        self.subsectors = nSubsectors
        self.costs = costs
        self.subsCoversList = self.calcSubsectorsCover(self.matrixDict)  # covers
        self.subsCoversOrdered = self.calcSubsectorsCoverDict(self.subsCoversOrdered)  # covers ordered

    def calcSubsectorsCover(self, matrixDict):
        """
        Return a list with number of sectors covered by subsectors (list position)
        """
        ret = []
        for x in range(self.subsectors):
            total = 0
            for y in matrixDict.keys():
                total = total + matrixDict[y][x]  # moving through sectors first
            ret.append(total)
        return ret

    def calcSubsectorsCoverDict(self, subsCoversList):
        """
        Return an ordered dictionary where key is subsector and value number of
        sectors covered by it
        """
        ret = {}
        for x in range(0, self.subsectors):  # -1 because list start at 0
            ret[x] = subsCoversList[x]
        return sorted(ret.items(), key=lambda t: t[1])  # ordered

    def getRatios(self):
        """
        Returns subsector ratio
        """
        ret = OrderedDict()
        for x in range(len(self.costs)):
            ret[x] = (self.subsCoversList[x] / self.costs[x])
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1]))  # ordered

    def setSectorsAtCovered(self, subsector, covered):
        """
        Given one subsector set each sectors covered by it as covered
        """
        for x in range(self.sectors):
            if (self.matrix[x][subsector] == 1):
                covered[x] += 1

    def delete(self, organism, covered):
        """
        Delete unnecessary subsectors a.k.a. hospitals
        """
        subsectors = self.getSelectedCovers(organism)
        for x in subsectors.keys():
            stop = False
            delete = False
            y = 0
            while not stop:
                if self.matrix[y][x] == 1:
                    if covered[y] - 1 == 0:
                        stop = True
                y += 1
                if y == self.sectors - 1:
                    delete = True
                    stop = True
            if delete:
                organism.genome[x] = "0"  # Delete item from solution

    def getSelectedCovers(self, organism):
        """
        Aux function for Delete, return ordered dict with covers only for
        selected subsectors
        """
        ret = OrderedDict()
        for x in range(self.subsectors):
            if organism.genome[x] == "1":
                ret[x] = self.subsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1], reverse=True))

    def recalculateMatrix(self, subsector, matrixDict, covered):
        """
        Recalculate matrix after select a subsector
        """
        self.setSectorsAtCovered(subsector, covered)
        self.subsCoversList[subsector] = 0
        delete=[]
        for x in matrixDict.keys():
            if(matrixDict[x][subsector] == 1):
                delete.append(x)
        for x in delete:
            matrixDict.pop(x,None)
        self.subsCoversList = self.calcSubsectorsCover()
        self.ratios = self.getRatios()

    def biggestCover(self, candidates):
        """
        Given candidates, return wich one has
        biggest cover value or random if equal
        """
        biggest = candidates[0]
        randomCandidates = []
        for x in candidates:  # x isn't index, x is subsector'
            if self.subsCoversList[x] > self.subsCoversList[biggest]:
                biggest = x
            elif self.subsCoversList[x] == self.subsCoversList[biggest] and biggest != x:
                randomCandidates.append(x)
        if (len(randomCandidates) > 0):
            randCandidate = random.randint(0, len(randomCandidates) - 1)
            biggest = randomCandidates[randCandidate]
        return biggest

    def select(self):
        """
        Returns the next subsector to be taken
        """
        stop = False
        candidates = []  # candidates to randomize
        fulllist = list(self.ratios.keys())  # all keys
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
        elif len(candidates) == 1:
            ret = candidates[0]
        return ret

    def repair(self, organism):
        new_organism = organism.copy()
        matrix_aux = copy.deepcopy(self.matrixDict)
        covered = list()  # Meaning each position is covered by X subsec
        self.ratios = self.getRatios()
        self.subsCoversList = self.calcSubsectorsCover()
        for x in range(self.sectors):
            self.covered.append(0)
        for x in range(self.subsectors):
            if new_organism.genome[x] == "1":
                self.setSectorsAtCovered(x, covered)
                matrix_aux.pop(x, None)
        if len(matrix_aux) > 0:
            # Sectors uncovered, greedy
            while len(self.neihtbourgMatrix) != 0:
                # Select candidates subsector for solution
                nextS = self.select()
                new_organism.genome[nextS] = "1"
                self.recalculateMatrix(nextS, matrix_aux, covered)
        else:
            # All sectors covered, return new_organism
            self.delete(new_organism, covered)
        return new_organism