from File import File
from Greedy import Greedy
from LocalSearch import LocalSearch
from Grasp import Grasp

import numpy as np

fichero = File('../instancias/scp41.txt')
fichero.leerDatos()

greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"1234")
greedy.start()

print("Solution cost GREEDY="+str(greedy.solCost))

# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "1234",10000)
# bl.start()
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))

grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"1234", 10000)
grasp.start()

print("Solution cost GREEDY="+str(greedy.solCost))
