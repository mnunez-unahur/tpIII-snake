import pygame
import random
import ia
from abc import ABC, abstractmethod
import networkx as nx
import matplotlib.pyplot as plt


DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
DIR_UP = 'UP'
DIR_DOWN = 'DOWN'

class Tablero():
    def __init__(self, ancho, alto,  tamCelda, color):
        self.alto = alto
        self.ancho = ancho
        self.cellSize = tamCelda
        self.color = color
        self.pantalla = pygame.display.set_mode(
            (self.anchoPx(), self.altoPx()))
        self.generarGrafo3()

    def altoPx(self):
        return self.alto * self.cellSize

    def anchoPx(self):
        return self.ancho * self.cellSize

    def centro(self):
        return self.ancho//2, self.alto//2

    def centroPx(self):
        return self.centro() * self.cellSize

    def limpiar(self):
        self.pantalla.fill(self.color)

    def dibujar(self, elemento, color):
        pygame.draw.rect(self.pantalla, color, elemento)

    def generarGrafo3(self):
        print("🔧 Generando grafo del tablero...", self.alto, self.ancho)
        self.grafo = nx.grid_2d_graph(self.ancho, self.alto)

    def mostrar_camino(self, path):

        nombre_archivo = "grafo_camino.png"
        # Crear figura proporcional al tamaño del tablero
        fig_w = self.ancho * self.cellSize / 100
        fig_h = self.alto * self.cellSize / 100
        plt.figure(figsize=(fig_w, fig_h))
        pos = {
            (x, y): (x * self.cellSize, y * self.cellSize)
            for x, y in self.grafo.nodes()
        }
        # Dibujar grafo base
        nx.draw(
            self.grafo,
            pos=pos,
            with_labels=False,
            node_size=10,
            node_color="black",
            edge_color="gray",
            linewidths=0.3
        )

        # Dibujar el camino (path)
        if path:
            nx.draw_networkx_nodes(
                self.grafo,
                pos,
                nodelist=path,
                node_color="yellow",
                node_size=30
            )
            # Dibuja el nodo de inicio (primer elemento del path)
            nx.draw_networkx_nodes(
                self.grafo,
                pos,
                nodelist=[path[0]],
                node_color="red",
                node_size=50,
                label="Inicio"
            )

            # Dibuja el nodo de destino (último elemento del path)
            nx.draw_networkx_nodes(
                self.grafo,
                pos,
                nodelist=[path[-1]],
                node_color="green",
                node_size=100,
                label="Destino"
            )

        # Ajustes visuales
        plt.axis("off")
        plt.axis("equal")

        # Guardar como imagen
        plt.gca().invert_yaxis() 
        plt.savefig(nombre_archivo, dpi=300, bbox_inches="tight")
        plt.close()

        print(f"✅ Camino guardado en '{nombre_archivo}'")


class Personaje(ABC):
    def __init__(self,
                 tablero,
                 direccionInicial=DIR_RIGHT,
                 x=0,
                 y=0,
                 colorCabeza=(255, 0, 0),
                 colorCuerpo=(255, 255, 0)):

        self.tablero = tablero
        self.size = tablero.cellSize
        self.detenido = True
        self.direccion = direccionInicial
        self.x = x
        self.y = y
        # indica que la siguiente vez que se mueva, el cuerpo debe crecer
        self.creceAlMover = False
        self.cuerpo = []
        self.colorCabeza = colorCabeza
        self.colorCuerpo = colorCuerpo
        self.puntos = 0

    # devuelve el rectangulo que ocupa el personaje
    def getRect(self):
        x = self.x * self.size
        y = self.y * self.size

        return pygame.Rect(x, y, self.size, self.size)

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
        self.cuerpo.append(self.getRect())

        if self.direccion == DIR_UP:
            self.y -= 1
        elif self.direccion == DIR_DOWN:
            self.y += 1
        elif self.direccion == DIR_RIGHT:
            self.x += 1
        else:
            self.x -= 1

        # salvo que haya comido, tengo que eliminar el ultimo segmento de la cola
        if not self.creceAlMover:
            self.cuerpo.pop(0)
        self.creceAlMover = False

    def hayColision(self, objeto):
        for rect in self.cuerpo:
            if rect.colliderect(objeto.getRect()):
                print(f"colision con {rect}")
                return True
        return False

    # alimentar al snake
    # incrementa el tamaño del cuerpo

    def alimentar(self):
        self.creceAlMover = True
        self.puntos += 1
        print(
            f" ********************** puntos: {self.puntos} *************************")

    def dibujar(self):
        for rect in self.cuerpo:
            self.tablero.dibujar(rect, self.colorCuerpo)
        self.tablero.dibujar(self.getRect(), self.colorCabeza)


class Humano(Personaje):
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
                 colorCabeza=(255, 0, 0),
                 colorCuerpo=(255, 255, 0)):

        self.comida = comida
        self.camino = []
        super().__init__(tablero, direccionInicial, x, y, colorCabeza, colorCuerpo)

    def determinarDireccion(self):
        if len(self.camino) == 0:
            start = (self.x, self.y)
            goal = (self.comida.x, self.comida.y)

            ancho_tablero = self.tablero.ancho
            alto_tablero = self.tablero.alto

            obstacles = {}
            for rect in self.cuerpo:
                x = int(rect.x / self.size)
                y = int(rect.y / self.size)
                obstacles[(x, y)] = True
            print(f"A*: {start, goal, self.tablero.grafo, ancho_tablero,
                         alto_tablero, obstacles}")
            path = ia.astar(start, goal, self.tablero.grafo, ancho_tablero,
                            alto_tablero, obstacles)
            self.tablero.mostrar_camino(path)

            if path == None:
                raise "error, path no encontrado"
            self.detenido = False

            # descarto el primero porque ya estoy en ese
            # sino hay colision con el cuerpo
            path.pop(0)
            self.camino = path
        return

    def mover(self):
        # si no no tiene un path definido, lo busco
        if len(self.camino) > 0:
            self.cuerpo.append(self.getRect())

            (self.x, self.y) = self.camino.pop(0)

            if not self.creceAlMover:
                self.cuerpo.pop(0)

        self.creceAlMover = False

        return


class Comida:
    def __init__(self, tablero, color=(0, 255, 0)):
        self.tablero = tablero
        self.size = tablero.cellSize
        self.color = color
        self.x = 0
        self.y = 0

    def reaparecer(self, snake):
        limite_derecho = self.tablero.ancho - 6
        limite_inferior = self.tablero.alto - 6

        self.x = random.randint(3, limite_derecho)
        self.y = random.randint(3, limite_inferior)

        # evitamos que la comida aparezca en el cuerpo
        while snake.hayColision(self):
            self.x = random.randint(2, limite_derecho)
            self.y = random.randint(2, limite_inferior)

        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        print(f"nueva comida en {rect}")

    def dibujar(self):
        self.tablero.dibujar(self.getRect(), self.color)

    # devuelve el rectangulo que ocupa la comida
    def getRect(self):
        x = self.x * self.size
        y = self.y * self.size

        return pygame.Rect(x, y, self.size, self.size)


class Muro():
    def __init__(self, tablero, grosor=20, color=(255, 255, 0)):
        self.color = color
        self.tablero = tablero
        self.muro = []

        ancho_tablero = tablero.pantalla.get_width()
        alto_tablero = tablero.pantalla.get_height()

        self.muro.append(pygame.Rect(0, 0, ancho_tablero, grosor))
        self.muro.append(pygame.Rect(ancho_tablero - grosor, 0,
                         ancho_tablero - grosor, ancho_tablero))
        self.muro.append(pygame.Rect(0, alto_tablero -
                         grosor, ancho_tablero, grosor))
        self.muro.append(pygame.Rect(0, 0, grosor, ancho_tablero))

    def dibujar(self):
        for rect in self.muro:
            self.tablero.dibujar(rect, self.color)

    # devuelve verdadero si hay colición del objeto rect con el muro
    def hayColision(self, objeto):
        for rect in self.muro:
            if rect.colliderect(objeto.getRect()):
                return True
        return False
