from random import choice, randint
from math import ceil

class Proceso:

    def __init__(self, id):

        self.op = choice(["+", "-", "*", "/", "%"])
        self.operando1 = randint(0, 99)             
        self.operando2 = randint(0, 99)

        if (self.operando2 == 0 and self.op == "/") or (self.operando2 == 0 and self.op == "/"):
            self.operando2 = randint(1, 99)

        self.TME = randint(6, 15)            
        self.id = id
        self.resultado = 0
        self.tam = randint(5, 25)           # Tamaño del proceso
        self.paginas = ceil(self.tam / 4)
        self.paginasEstables = self.paginas
        self.TT = 0
        self.TR = self.TME
        self.TTB = 0
        self.TLlegada = 0
        self.TFinalizacion = 0
        self.TRetorno = 0
        self.TRespuesta = 0
        self.TEspera = 0
        self.TServicio = 0
        self.banderaRespuesta = False

    def calcularResulrado(self):

        if self.op == "+":
            return self.operando1 + self.operando2
        elif self.op == "-":
            return self.operando1 - self.operando2
        elif self.op == "*":
            return self.operando1 * self.operando2
        elif self.op == "/":
            return self.operando1 / self.operando2
        elif self.op == "%":
            return self.operando1 % self.operando2