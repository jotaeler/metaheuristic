import random
import copy
from collections import OrderedDict
from Bio.GA import Organism
from Bio.Seq import MutableSeq
#from Bio.GA.Selection import Tournament
from Tournament import TournamentSelection
from AlphabetSCP import AlphabetSCP
from Bio.GA.Mutation import Simple
from Bio.GA.Crossover import Uniform
from Bio.GA.Evolver import GenerationEvolver
from repair import Repair


class Generation(object):

    def __init__(self, costs, matrix, sectors, subsectors):
        random.seed("1234")
        self.costs = costs  # List with cost of each subsector
        self.sectors = sectors  # Int, number of sectors
        self.subsectors = subsectors  # Int, number of subsectors
        self.matrix = matrix  # Bin matrix meaning wich subsctr covers each sec
        self.matrixDict = {}
        self.subsCoversList = []  # covers
        self.subsCoversOrdered = {}  # covers ordered
        self.covered = list()  # Meaning each position is covered by X subsec
        self.iterations = 0

    def stop(self, population):
        """
        Stopping criteria for evolution process
        :return:
        """
        print("Stopping criteria function iterations = "+str(self.iterations))
        if self.iterations < 20000:
            return False
        else:
            return True


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

    def setSectorsAtUnCovered(self, subsector):
        """
        Given one subsector set each sectors covered by it as UNcovered
        """
        for x in range(self.sectors):
            if (self.matrix[x][subsector] == 1):
                self.covered[x] -= 1

    def setSectorsAtCovered(self, subsector):
        """
        Given one subsector set each sectors covered by it as covered
        """
        for x in range(self.sectors):
            if (self.matrix[x][subsector] == 1):
                self.covered[x] += 1

    def delete(self, seq):
        """
        Delete unnecessary subsectors a.k.a. hospitals
        """
        subsectors = self.getSelectedCovers(seq)
        for x in subsectors.keys():
            stop = False
            delete = False
            y = 0
            while not stop :
                if self.matrix[y][x] == 1:
                    if self.covered[y]-1 == 0:
                        stop = True
                y += 1
                if y == self.sectors-1:
                    delete = True
                    stop = True
            if delete :
                self.setSectorsAtUnCovered(x)
                seq[x] = "0"  # Delete item from solution

    def getSelectedCovers(self, seq):
        """
        Aux function for Delete, return ordered dict with covers only for
        selected subsectors
        """
        ret = OrderedDict()
        for x in range(self.subsectors):
            if seq[x] == "1":
                ret[x] = self.subsCoversOrdered[x]
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1], reverse=True))

    def recalculateMatrix(self, subsector):
        """
        Recalculate matrix after select a subsector
        """
        self.setSectorsAtCovered(subsector)
        self.subsCoversList[subsector] = 0
        delete = []
        for x in self.matrixDict.keys():
            if (self.matrixDict[x][subsector] == 1):
                delete.append(x)
        for x in delete:
            self.matrixDict.pop(x, None)

    def calcNObjNoCov(self):
        """
        Return a list with number of sectors covered by subsectors (list position)
        """
        ret = 0
        for x in range(self.subsectors):
            if self.subsCoversList[x] > ret:
                ret = self.subsCoversList[x]
        return ret

    def randomizedGreedy(self):
        """
        Generate Genome through Randomize Greedy through RCL list
        """
        print("randomizedGreedy")
        for x in range(self.sectors):
            self.matrixDict[x] = self.matrix[x]
        self.subsCoversList = self.calcSubsectorsCover()  # covers
        self.subsCoversOrdered = self.calcSubsectorsCoverDict()  # covers ordered
        self.covered = list()
        for x in range(self.sectors):
            self.covered.append(0)
        solution = "0"*self.subsectors
        seq = MutableSeq(solution,AlphabetSCP())
        while len(self.matrixDict) != 0:
            rcl = []
            MaxObjCov = self.calcNObjNoCov() * 0.7
            rand = 0
            for x in range(self.subsectors):
                if self.subsCoversList[x] >= MaxObjCov:
                    rcl.append(x)
            if len(rcl) > 1:
                rand = random.randint(0, len(rcl) - 1)
            candidate = rcl[rand]
            seq[candidate] = "1"
            self.recalculateMatrix(candidate)
        self.delete(seq)
        return seq

    def getCost(self, genome):
        """
        Calc Genome Cost genome object is MutableSeq
        """
        print("Call to fitness function")
        total = 0
        self.iterations += 1
        for x in range(self.subsectors):
            if genome[x] == "1":
                total += self.costs[x]
        return total

    def runGenerationEvolverHUX(self):
        """
        Run the algorithm with Uniform crossover
        :return:
        """
        population = Organism.function_population(self.randomizedGreedy, 50, self.getCost)
        mutator = Simple.ConversionMutation(0.01)
        crossover = Uniform.UniformCrossover(1, 0.7)
        repairer = Repair(self.matrix, self.sectors, self.subsectors, self.costs)

        selector = TournamentSelection(mutator, crossover, repairer, 2)
        evolver = GenerationEvolver(population, selector)
        final_population = evolver.evolve(self.stop)
        return final_population