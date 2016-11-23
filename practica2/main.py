from generation import Generation
from File import File
import time

fichero = File('../instancias/scp41.txt')
fichero.leerDatos()

generacional = Generation(fichero.costs, fichero.binMatrix, fichero.rows, fichero.columns)
t0 = time.clock()
poblacion_evolucionada = generacional.runGenerationEvolverHUX()
end = time.clock() -t0
print("Ejecucion  = "+str(end))
print(str(poblacion_evolucionada[0].fitness))



