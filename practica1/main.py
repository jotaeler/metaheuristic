from File import File
from Greedy import Greedy
from LocalSearch import LocalSearch
from Grasp import Grasp
from TabuSearch import TabuSearch

# import numpy as np

fichero = File('../instancias/scp41.txt')
fichero.leerDatos()

greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"1234")
greedy.start()

#print("Covered= "+str(greedy.covered))
# print("Solution= "+str(greedy.solution))
# print("Solution cost="+str(greedy.solCost))

print("Solution cost GREEDY="+str(greedy.solCost))

# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "1234",10000)
# bl.start()
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))

grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"1234", 10000)
grasp.start()

print("Solution cost GRASAP="+str(grasp.bestSolutionCost))

# bt = TabuSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "1234", 10000)
# bt.start()
# print("Busqueda Tabu coste de la solucion: "+str(bt.bestSolutionCost))
