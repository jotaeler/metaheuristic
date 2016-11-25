from generation import Generation
from File import File
import time

fichero = File('../instancias/scpa1.txt')
fichero.leerDatos()

generacional = Generation(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns)
t0 = time.clock()
poblacion_evolucionada = generacional.runGenerationEvolverHUX()
best = poblacion_evolucionada[0]
for organism in poblacion_evolucionada:
    if organism.fitness < best.fitness:
        best = organism
end = time.clock() -t0
print("Ejecucion  = "+str(end))
print(str(best.fitness))



