class Move:
    def __init__(self, solucionActual, solucionVecina):
        self.quitarMovimiento = -1  #indice de la solucion que quitamos
        self.listaAñadirMovimiento = []  #Lista de indices que vamos añadiendo a la solucion
        self.solucionActual = solucionActual    #Lista con la solucion que estamos trabajando
        self.solucionVecina = solucionVecina    #Lista con la solucion vecina, generado con el algoritmo

    """
    Metodo para comparar los movimientos
    :return booleano, True en caso que sean iguales, False en caso contrario
    """
    # def compararMovimientos(self, move):
    #     if(self.quitarMovimiento == move.quitarMovimiento
    #        and self.listaAñadirMovimiento == move.listaAñadirMovimiento):
    #         return True
    #     else:
    #         return False

    """
    Metodo para calcular los movimientos
    """
    def calcularMovimientos(self):
        quita = 0
        for i in range(len(self.solucionActual)):
            if self.solucionActual[i] != self.solucionVecina[i]:
                if int(quita) == 0:
                    self.quitarMovimiento = i
                    quita += 1
                else:
                    self.listaAñadirMovimiento.append(i)









