from Bio.GA import Organism
import copy
from collections import OrderedDict

class Repair(object):

    def __init__(self, matrix, nSectors, nSubsectors, costs):
        self.matrix = matrix
        self.matrixDict = {}
        for x in range(self.sectors):
            self.matrixDict[x] = self.matrix[x]
        self.sectors = nSectors
        self.subsectors = nSubsectors
        self.costs = costs
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.subsCoversOrdered = self.calcSubsectorsCoverDict()  # covers ordered



    def calcSubsectorsCover(self):
        """
        Return a list with number of sectors covered by subsectors (list position)
        """
        ret = []
        for x in range(self.subsectors):
            total = 0
            for y in self.matrixDict.keys():
                total = total + self.matrixDict[y][x]  # moving through sectors first
            ret.append(total)
        return ret

    def calcSubsectorsCoverDict(self):
        """
        Return an ordered dictionary where key is subsector and value number of
        sectors covered by it
        """
        ret = {}
        for x in range(0, self.subsectors):  # -1 because list start at 0
            ret[x] = self.subsCoversList[x]
        return sorted(ret.items(), key=lambda t: t[1])  # ordered



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


    def getSelectedCovers(self, organism, subsCoversOrdered):
        """
        Aux function for Delete, return ordered dict with covers only for
        selected subsectors
        """
        ret = OrderedDict()
        for x in range(self.subsectors):
            if organism.genome[x] == "1":
                ret[x] = self.subsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1], reverse=True))

    def recalculateMatrix(self, subsector):
        """
        Recalculate matrix after select a subsector
        """
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


    def select(self, ratios):
        """
        Returns the next subsector to be taken
        """
        stop = False
        candidates = []  # candidates to randomize
        fulllist = list(ratios.keys())  # all keys
        reverseIndex = -2
        index = 0
        candidates.append(fulllist[-1])  # key of biggest ratio
        ret = 0
        while not(stop):
            if ratios[candidates[index]] == ratios[fulllist[reverseIndex]]:
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
        for x in range(self.subsectors):
            if new_organism.genome[x] == "1":
                self.setSectorsAtCovered(x, covered)
                matrix_aux.pop(x, None)
        if len(matrix_aux) > 0:
            # Sectors uncovered, greedy
            while len(self.neihtbourgMatrix) != 0:
                # Select candidates subsector for solution
                nextS=self.select()
                new_organism.genome[nextS] = "1"
                self.recalculateMatrix(nextS)
        else:
            # All sectors covered, return new_organism
            self.delete(new_organism, covered)
        return new_organism