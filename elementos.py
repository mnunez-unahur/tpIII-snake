import pygame
import random
import ia

from abc import ABC, abstractmethod


DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
DIR_UP = 'UP'
DIR_DOWN = 'DOWN'

class Personaje(ABC):
    def __init__(self,
        tablero,
        direccionInicial=DIR_RIGHT, 
        x=0, 
        y=0, 
        cellSize = 10, 
        colorCabeza=(255, 0, 0), 
        colorCuerpo=(255, 255, 0)):

        self.tablero = tablero
        self.detenido = True
        self.direccion = direccionInicial
        self.x = x
        self.y = y
        # indica que la siguiente vez que se mueva, el cuerpo debe crecer
        self.creceAlMover = False
        self.cola=[]
        self.cellSize = cellSize
        self.colorCabeza = colorCabeza
        self.colorCuerpo = colorCuerpo
        self.puntos = 0

    # devuelve el rectangulo que ocupa el personaje
    def getRect(self):
        x = self.x * self.cellSize
        y = self.y * self.cellSize

        return pygame.Rect(x, y, self.cellSize, self.cellSize)

    # determina la siguiente dirección del personaje
    @abstractmethod
    def determinarDireccion(self):
        pass

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


    def hayColision(self, objeto):
        for rect in self.cola:
            if rect.colliderect(objeto.getRect()):
                print(f"colision con {rect}")
                return True
        return False


    # alimentar al snake
    # incrementa el tamaño del cuerpo
    def alimentar(self):
        self.creceAlMover = True
        self.puntos += 1
        print(f" ********************** puntos: {self.puntos} *************************")

    def dibujar(self, tablero):
        for rect in self.cola:
            pygame.draw.rect(tablero, self.colorCuerpo, rect)
        pygame.draw.rect(tablero, self.colorCabeza, self.getRect())




class Humano(Personaje):
    # def __init__(self, 
    #     direccionInicial=DIR_RIGHT, x=0, y=0, cellSize = 10, colorCabeza=(255, 0, 0), colorCuerpo=(255, 255, 0)):

    #     super().__init__(direccionInicial,x, y, cellSize, colorCabeza, colorCuerpo)
    
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
    def __init__(self,
        tablero,
        comida,
        direccionInicial=DIR_RIGHT, 
        x=0, y=0, 
        cellSize = 10, 
        colorCabeza=(255, 0, 0), 
        colorCuerpo=(255, 255, 0)):

        self.comida = comida
        self.path = []
        super().__init__(tablero, direccionInicial,x, y, cellSize, colorCabeza, colorCuerpo)
    
    def determinarDireccion(self):
        if len(self.path) == 0:
            start = (self.x, self.y)
            goal = (self.comida.x, self.comida.y)

            ancho_tablero = int(self.tablero.get_width() / self.cellSize)
            alto_tablero = int(self.tablero.get_height() / self.cellSize)

            obstacles = {}
            print(f"cola: {self.cola}")
            for rect in self.cola:
                x = int(rect.x / self.cellSize)
                y = int(rect.y / self.cellSize)
                obstacles[(x, y)] = True

            path = ia.astar(start, goal, ancho_tablero,
                                alto_tablero, obstacles)

            print(f">>>>> path: {path} ")

            if path == None:
                raise "error, path no encontrado"
            self.detenido = False

            # descarto el primero porque ya estoy en ese
            # sino hay colision con el cuerpo
            path.pop(0) 
            self.path = path
        return

    def mover(self):
        # si no no tiene un path definido, lo busco
        if len(self.path) > 0:
            self.cola.append(self.getRect())

            (self.x, self.y) = self.path.pop(0)

            if not self.creceAlMover:
                self.cola.pop(0)
                
        self.creceAlMover = False

        return


class Comida:
    def __init__(self, cellSize = 10, color=(0, 255, 0)):
        self.color = color
        self.cellSize = cellSize
        self.x = 0
        self.y = 0

    def reaparecer(self, tablero, snake):
        self.x = random.randint(
            2, int(tablero.get_width()/self.cellSize) -4)
        self.y = random.randint(
            2, int(tablero.get_height()/self.cellSize) -4)

        # evitamos que la comida aparezca en el cuerpo
        while snake.hayColision(self):
            self.x = random.randint(
                2, int(tablero.get_width()/self.cellSize) -4)
            self.y = random.randint(
                2, int(tablero.get_height()/self.cellSize) -4)
        
        rect = pygame.Rect(self.x, self.y, self.cellSize, self.cellSize)      
        print(f"nueva comida en {rect}")


    def dibujar(self, tablero):
        pygame.draw.rect(tablero, self.color, self.getRect())


    # devuelve el rectangulo que ocupa la comida
    def getRect(self):
        x = self.x * self.cellSize
        y = self.y * self.cellSize

        return pygame.Rect(x, y, self.cellSize, self.cellSize)

class Muro():
    def __init__(self, tablero, grosor=20, color=(255, 255, 0)):
        self.color = color
        self.muro = []

        ancho_tablero = tablero.get_width()
        alto_tablero = tablero.get_height()

        self.muro.append(pygame.Rect(0, 0, ancho_tablero, grosor))
        self.muro.append(pygame.Rect(ancho_tablero - grosor, 0, ancho_tablero - grosor, ancho_tablero))
        self.muro.append(pygame.Rect(0, alto_tablero - grosor, ancho_tablero, grosor))
        self.muro.append(pygame.Rect(0, 0, grosor, ancho_tablero))

    def dibujar(self, tablero):
        for rect in self.muro:
            pygame.draw.rect(tablero, self.color, rect)

    # devuelve verdadero si hay colición del objeto rect con el muro
    def hayColision(self, objeto):
        for rect in self.muro:
            if rect.colliderect(objeto.getRect()):
                return True
        return False
