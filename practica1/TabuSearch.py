from collections import OrderedDict
from practica1.LocalSearch import LocalSearch
import random
import copy
from practica1.Move import Move

random.seed("1234")

class TabuSearch:
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
        self.tabuList = list()
        self.limit = limit

    """
    Generar vecino
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
            if subsector+1 >= len(candidatesToRand):
                subsector=0
            else:
                rand = subsector+1
                subsector = candidatesToRand[subsector+1]
        if subsector == arg['firstRand'] and firstRand == False:
            stop = True
        else:
            neihtbourg['solution'] = copy.deepcopy(solution)
            #delete rows covered
            delete=[]
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
            while not(stop) and len(self.neihtbourgMatrix) != 0:
                # Select candidates subsector for solution
                nextS=self.select()
                if nextS == None :
                    stop=True
                else:
                    neihtbourg['solution'][nextS] = 1
                    cost += self.costs[nextS]
                    self.recalculateMatrix(nextS)
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
    Returns subsector ratio
    """
    def getRatios(self):
        ret = OrderedDict()
        for x in range(len(self.costs)):
            ret[x] = (self.neihSubsCoversList[x]/self.costs[x])
        return OrderedDict(sorted(ret.items(), key=lambda t: t[1]))   # ordered

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
        while not(stop):
            if self.neihRatios[candidates[index]] == self.neihRatios[fulllist[reverseIndex]]:
                index += 1
                candidates.append(fulllist[reverseIndex])
                reverseIndex-=1
            else:
                stop = True
        if(len(candidates) > 1):
            ret = self.biggestCover(candidates)
        elif len(candidates) == 1:
            ret=candidates[0]
        else:
            ret=None
        return ret

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
    Metodo para ver si el movimiento ya existe en tabu
    """
    def estaMovimiento(self, move):
        for i in range(len(self.tabuList)):
            if(self.tabuList[i] == move):
                return move
        return None

    """
    Metodo para calcular el NumGreedySet
    """
    def numGreedySet(self):
        numSet = 0
        for i in range(len(self.bestSolution)):
            if (self.bestSolution[i] == 1):
                numSet += 1
        return  numSet

    """
    devuelve el indice donde se encuentra el movimiento
    """
    def buscarIndice(self, move):
       indice = 0
       for i in range(len(self.tabuList)):
           if (i == move):
               return i
           else:
               indice += 1


    """
    Metodo para reordenar la lista tabu
    """
    def reordenarLista(self, move):
        indice = self.buscarIndice(move)
        posAnt = indice
        posIndice = indice
        for i in range(indice):
            posAnt -= 1
            self.tabuList[posIndice] = self.tabuList[posAnt]
            posIndice -= 1
            if posAnt == 0:
                break

    def generarVecinos(self, numVecinos):
        mejorCosteVecino = 99999
        vecinoOK = list()
        neihtbourg= {'solution':self.bestSolution, 'cost':self.bestSolutionCost,'subsector': -1,'continue':True, 'firstRand':-1}

        for i in range(numVecinos): #Genero los 50 vecinos y eligo el mejor de ellos
            neihtbourg = self.genNeihtbourg(neihtbourg)
            costeAux = neihtbourg['cost']
            if (costeAux < int(mejorCosteVecino)):
                neihtbourg['subsector'] = -1
                neihtbourg['firstRand'] = -1
                vecinoOK = copy.deepcopy(neihtbourg['solution'])
                mejorCosteVecino = neihtbourg['cost']
                neihtbourg['solution'] = vecinoOK
                self.updateMemory(False)
            else:
                self.updateMemory(True)
            if (costeAux >= self.bestSolutionCost):
                break
        return vecinoOK, mejorCosteVecino

    """
    Returns the solution
    """
    def start(self):
        iterations = 0
        TSFactor = 0.8
        mejorVecino = list()
        mejorCoste = 0
        tamListaTabu = TSFactor * self.numGreedySet() + 1
        stop = False
        #neihtbourg= {'solution':self.bestSolution, 'cost':self.bestSolutionCost,'subsector': -1,'continue':True, 'firstRand':-1}
        while not(stop or self.bestSolutionCost < mejorCoste):
            mejorVecino, mejorCoste = self.generarVecinos(50)
            move = Move(self.bestSolution, mejorVecino) #Creo el movimiento
            move.calcularMovimientos()  #Calculo el movimiento
            if(len(self.tabuList) > 0): #Si hay algun movimiento en la lista tabu
                moveAux = self.estaMovimiento(move) #Devuelve el movimiento en caso que este en la lista, o None en caso contrario
                if moveAux != None:
                    if(mejorCoste < self.bestSolutionCost): #Compruebo si la solucion vecina mejora a la solucion actual
                        self.bestSolution = copy.deepcopy(mejorVecino)
                        self.bestSolutionCost=mejorCoste
                        self.updateMemory(False)
                        self.reordenarLista(moveAux)
                    else:
                        self.updateMemory(True)
                else:   #No esta en la lista tabu, pero el vecino mejora a la mejor solucion actual
                    if(mejorCoste < self.bestSolutionCost):
                        self.bestSolution = copy.deepcopy(mejorVecino)
                        self.bestSolutionCost=mejorCoste
                        self.updateMemory(False)
                    else:
                        self.updateMemory(True)
                    if (len(self.tabuList) == int(tamListaTabu)):   #Compruebo si la lista ha llegado a su tamaño maximo
                        self.tabuList.pop(int(tamListaTabu) - 1) #Elimino el movimiento de la ultima posicion
                        self.tabuList.append(move)
                    else:
                        self.tabuList.append(move)
            else:   #Es el primer movimiento, asi que lo añado a la lista tabu
                if(mejorCoste < self.bestSolutionCost): #Compruebo si el vecino mejora a la mejor solucion actual
                        self.bestSolution = copy.deepcopy(mejorVecino)
                        self.bestSolutionCost=mejorCoste
                        self.updateMemory(False)
                else:
                    self.updateMemory(True)
                self.tabuList.append(move)
            iterations += 1
            if iterations == 10000:
                stop=True


