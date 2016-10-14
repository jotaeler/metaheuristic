from File import File
from Greedy import Greedy

fichero = File('../instancias/scp41.txt')
fichero.leerDatos()

#print ('Matriz ' + str(fichero.binMatrix))
print('Numero de datos que hay en el fichero: ' + fichero.num.__str__())
print('Numero de comisarias: ' + fichero.columns.__str__())
print('Numero de ciudades: ' + fichero.rows.__str__())
print('El numero de datos que tiene los costes son: ' + str(fichero.costs.__len__()))

greedy = Greedy(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns)
greedy.start()
print("Covered= "+str(greedy.covered))
print("Solution= "+str(greedy.solution))
