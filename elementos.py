import pygame
from abc import ABC, abstractmethod


DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
DIR_UP = 'UP'
DIR_DOWN = 'DOWN'

class Personaje(ABC):
    def __init__(self, direccionInicial=DIR_RIGHT, x=0, y=0, cellSize = 10, tablero=None, colorCabeza=(255, 0, 0), colorCuerpo=(255, 255, 0)):
        self.detenido = True
        self.direccion = direccionInicial
        self.x = x
        self.y = y
        # indica que la siguiente vez que se mueva, el cuerpo debe crecer
        self.creceAlMover = False
        self.cola=[]
        self.cellSize = cellSize
        self.tablero = tablero
        self.colorCabeza = colorCabeza
        self.colorCuerpo = colorCuerpo

    # devuelve el rectangulo que ocupa el personaje
    def getRect(self):
        x = self.x * self.cellSize
        y = self.y * self.cellSize

        return pygame.Rect(x, y, self.cellSize, self.cellSize)


    # ejecuta un movimiento del jugador
    def tick(self):
        self.determinarDireccion()

        # si está detenido no hago nada
        if self.detenido:
            return

        self.mover()

    def mover(self):
        # agregamos la celda actual en la cola para poder dibujarla
        self.cola.append(self.getRect())
            
        if self.direccion == DIR_UP:
            self.y -= 1
        elif self.direccion == DIR_DOWN:
            self.y += 1
        elif self.direccion == DIR_RIGHT:
            self.x += 1
        else:
            self.x -=1
        
        # salvo que haya comido, tengo que eliminar el ultimo segmento de la cola
        if not self.creceAlMover:
            self.cola.pop(0)
        self.creceAlMover = False


    def hayColisionConCuerpo(self):
        for rect in self.cola:
            if self.getRect().colliderect(rect):
                return True
        return False


    # determina la siguiente dirección del personaje
    @abstractmethod
    def determinarDireccion(self):
        pass

    # alimentar al snake
    # incrementa el tamaño del cuerpo
    def alimentar(self):
        self.creceAlMover = True

    def dibujar(self):
        for rect in self.cola:
            pygame.draw.rect(self.tablero, self.colorCuerpo, rect)
        pygame.draw.rect(self.tablero, self.colorCabeza, self.getRect())



class Humano(Personaje):
    def __init__(self, direccionInicial=DIR_RIGHT, x=0, y=0, cellSize = 10, tablero=None, colorCabeza=(255, 0, 0), colorCuerpo=(255, 255, 0)):
        super().__init__(direccionInicial,x, y, cellSize, tablero, colorCabeza, colorCuerpo)
    
    def determinarDireccion(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direccion = DIR_LEFT
            self.detenido = False
        if keys[pygame.K_RIGHT]:
            self.direccion = DIR_RIGHT
            self.detenido = False
        if keys[pygame.K_UP]:
            self.direccion = DIR_UP
            self.detenido = False
        if keys[pygame.K_DOWN]:
            self.direccion = DIR_DOWN
            self.detenido = False


class IA(Personaje):
    def __init__(self, direccionInicial=DIR_RIGHT, x=0, y=0, cellSize = 10, tablero=None, colorCabeza=(255, 0, 0), colorCuerpo=(255, 255, 0)):
        super().__init__(direccionInicial,x, y, cellSize, tablero, colorCabeza, colorCuerpo)
    
    def determinarDireccion(self):
        # pasos
        # 1 - si no tiene un camino establecido, ejecutar algoritmo y usar el primer paso
        # 2 - si ya tiene un camino establecido, usar el primer paso
        return

    def determinarDireccion(self):
        super.mover()
        # despues de mover, debería eliminar el primer elemento del camino establecido
        return


