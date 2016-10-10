class File:
    """
    Constructor de la clase, el parametro que se pasa
    es la direccion del fichero que queremos leer
    """
    def __init__(self, path):
        self.path = path        #Path donde se encuentra el fichero a cargar
        self.costs = []         #Array de costes
        self.binMatrix = []     #Matriz bidimensional, relacion (ciudades - comisarias)
        self.rows = 0           #Numero de ciudades
        self.columns = 0        #Numero de comisarias
        self.num = 0            #Numero total de datos del fichero
        self.totalDatos = []    #Array con todos los datos cargados del fichero

    """
    Metodo para leer los datos del fichero que se le pasa en el constructor
    """
    def leerDatos(self):
        infile = open(self.path, 'r')
        for line in infile:
            palabras = line.split()
            for p in palabras:
                self.totalDatos.append(p)
                self.num += 1
        infile.close()
        self.rows = int(self.totalDatos[0])  # Numero de filas
        self.columns = int(self.totalDatos[1])  # Numero de columnas

        for i in range(self.rows):
                self.binMatrix.append([0]*self.columns) #relleno la matriz con ceros

        #Calculo los costes
        contador = self.getColumns() + 2
        for i in range(2, contador):
            # guardo los costes
            self.costs.append(self.totalDatos[i])

        #Calculo la matriz bidimensional
        ciudad = 0
        datosCiudad = 0
        for i in range(1003,self.num):
            if datosCiudad < int(self.totalDatos[1002]):
                self.binMatrix[int(ciudad)][int(self.totalDatos[i])-1] = 1
                datosCiudad += 1
            elif datosCiudad == 0:
                ciudad += 1
                datosCiudad = self.totalDatos[i]

    """
    Metodo para devolver el numero de filas
    """
    def getRows(self):
        return self.rows

    """
    Metodo para devolver el numero de columnas
    """
    def getColumns(self):
        return self.columns

    """
    Muestra los datos que hay guardados en el array 'Cost'
    """
    def mostrarCostes(self):
        for i in range(self.costs.__len__()):
            print  self.costs[i]

    """
    Muestra los datos de la matriz "binMatrix"
    """
    def mostrarMatriz(self):
        print self.binMatrix

# fichero = File('../instancias/scp41.txt')
# fichero.leerDatos()
#
# print 'Numero de ciudades: ' + fichero.rows.__str__()
# print 'Numero de comisarias: ' + fichero.columns.__str__()
# print 'Numero de datos que hay en el fichero: ' + fichero.num.__str__()
# print 'El numero de datos que tiene los costes son: ' + str(fichero.costs.__len__())
#
# fichero.mostrarMatriz()
