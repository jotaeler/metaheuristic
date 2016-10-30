from File import File
from Greedy import Greedy
from LocalSearch import LocalSearch
from Grasp import Grasp
import time


fichero = File('../instancias/scpnrf1.txt')
fichero.leerDatos()

# t0 = time.clock()
# greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"77373014")
# greedy.start()
# end = time.clock() -t0
# print("Ejecucion 1 = "+str(end))
# print("Solution cost GREEDY="+str(greedy.solCost))
# print("-------------------------------------------")

# t0 = time.clock()
# greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"47737301")
# greedy.start()
# end = time.clock() -t0
# print("Ejecucion 2 = "+str(end))
# print("Solution cost GREEDY="+str(greedy.solCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"14773730")
# greedy.start()
# end = time.clock() -t0
# print("Ejecucion 3 = "+str(end))
# print("Solution cost GREEDY="+str(greedy.solCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"01477373")
# greedy.start()
# end = time.clock() -t0
# print("Ejecucion 4 = "+str(end))
# print("Solution cost GREEDY="+str(greedy.solCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"30147737")
# greedy.start()
# end = time.clock() -t0
# print("Ejecucion 5 = "+str(end))
# print("Solution cost GREEDY="+str(greedy.solCost))
# print("-------------------------------------------")
# t0 = time.clock()
# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "77373014",10000)
# bl.start()
# end = time.clock() -t0
# print("Ejecucion 1 = "+str(end))
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "47737301",10000)
# bl.start()
# end = time.clock() -t0
# print("Ejecucion 2 = "+str(end))
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "14773730",10000)
# bl.start()
# end = time.clock() -t0
# print("Ejecucion 3 = "+str(end))
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "01477373",10000)
# bl.start()
# end = time.clock() -t0
# print("Ejecucion 4 = "+str(end))
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))
# print("-------------------------------------------")
#
# t0 = time.clock()
# bl=LocalSearch(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns, greedy.solution, greedy.solCost, greedy.covered, "30147737",10000)
# bl.start()
# end = time.clock() -t0
# print("Ejecucion 5 = "+str(end))
# print("Busqueda LOCAL Solution cost="+str(bl.bestSolutionCost))
# print("-------------------------------------------")
t0 = time.clock()
grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"77373014", 10000)
grasp.start()
end = time.clock() -t0
print("Ejecucion 1 = "+str(end))
print("Solution cost GRASP="+str(grasp.bestSolutionCost))
print("-------------------------------------------")

t0 = time.clock()
grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"47737301", 10000)
grasp.start()
end = time.clock() -t0
print("Ejecucion 2 = "+str(end))
print("Solution cost GRASP="+str(grasp.bestSolutionCost))
print("-------------------------------------------")

t0 = time.clock()
grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"14773730", 10000)
grasp.start()
end = time.clock() -t0
print("Ejecucion 3 = "+str(end))
print("Solution cost GRASP="+str(grasp.bestSolutionCost))
print("-------------------------------------------")

t0 = time.clock()
grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"01477373", 10000)
grasp.start()
end = time.clock() -t0
print("Ejecucion 4 = "+str(end))
print("Solution cost GRASP="+str(grasp.bestSolutionCost))
print("-------------------------------------------")

t0 = time.clock()
grasp = Grasp(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns,"30147737", 10000)
grasp.start()
end = time.clock() -t0
print("Ejecucion 5 = "+str(end))
print("Solution cost GRASP="+str(grasp.bestSolutionCost))
