from practica1.File import File

def main():
    fichero = File('../instancias/scp41.txt')
    fichero.leerDatos()

    print 'Numero de ciudades: ' + fichero.rows.__str__()
    print 'Numero de comisarias: ' + fichero.columns.__str__()
    print 'Numero de datos que hay en el fichero: ' + fichero.num.__str__()
    print 'El numero de datos que tiene los costes son: ' + str(fichero.costs.__len__())

    # print fichero.mostrarMatriz()


if __name__ == '__main__':
    main()
