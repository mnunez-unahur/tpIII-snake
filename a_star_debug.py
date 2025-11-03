import pygame
import juego
from heapq import heappush, heappop
import networkx as nx

pygame.init()

CELL_SIZE = 15
ANCHO, ALTO = 64, 48  # cantidad de celdas, no pixeles
pantalla = pygame.display.set_mode((ANCHO*CELL_SIZE, ALTO*CELL_SIZE))
pantalla.fill((0, 0, 0))

cuadro_alpha = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
cuadro_alpha.fill((255, 182, 193, 100))


def init():
    cuerpo = []
    cuerpo_alpha = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
    # Gris con alpha 100 (semi-transparente)
    cuerpo_alpha.fill((200, 200, 200, 50))
    tablero = juego.Tablero(ANCHO, ALTO, CELL_SIZE, (50, 50, 50))
    xInicial, yInicial = tablero.centro()
    comida = juego.Comida(tablero, color=(0, 255, 0))
    muro = juego.Muro(tablero, color=(150, 150, 50))
    snake = juego.IA(tablero, comida, colorCabeza=(255, 0, 0), colorCuerpo=(
        255, 255, 0), x=xInicial, y=yInicial, debug=False)
    comida.reaparecer(snake)

    grafo = nx.grid_2d_graph(ANCHO, ALTO)
    inicio = (snake.x, snake.y)
    destino = (comida.x, comida.y)

    astar_gen = astar_debug_tick(inicio, destino, grafo, {})

    clock = pygame.time.Clock()
    salir = False

    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True

        pantalla.fill((0, 0, 0))
        tablero.limpiar()
        muro.dibujar()
        snake.dibujar()
        comida.dibujar()

        try:
            tipo, nodo = next(astar_gen)
            print(tipo)
            if tipo == "vecino":
                pantalla.blit(
                    cuadro_alpha, (nodo[0]*CELL_SIZE, nodo[1]*CELL_SIZE))
            elif tipo == "fin":
                ruta = nodo
                for pos in ruta:
                    pygame.draw.rect(
                        pantalla, (100, 255, 100), (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif "node_actual":
                snake.tick()

            cuerpo.append((snake.x*CELL_SIZE, snake.y *
                           CELL_SIZE, CELL_SIZE, CELL_SIZE))
            for segmento in cuerpo:
                pantalla.blit(cuerpo_alpha, segmento)
        except StopIteration:

            pass

        pygame.display.flip()
        clock.tick(20)


def astar_debug_tick(inicio, destino, grafo, obstaculos):

    lista_abierta = []
    heappush(lista_abierta, (0, inicio))
    viene_de = {}
    g_costo = {inicio: 0}

    while lista_abierta:
        _, nodo_actual = heappop(lista_abierta)
        yield ("nodo_actual", nodo_actual)

        if nodo_actual == destino:
            ruta = []
            while nodo_actual in viene_de:
                ruta.append(nodo_actual)
                nodo_actual = viene_de[nodo_actual]
            ruta.append(inicio)
            ruta.reverse()
            yield ("fin", ruta)
            return

        for vecino in grafo.neighbors(nodo_actual):
            if vecino in obstaculos and vecino != destino:
                continue

            g_candidato = g_costo[nodo_actual] + 1

            if g_candidato < g_costo.get(vecino, float('inf')):
                viene_de[vecino] = nodo_actual
                g_costo[vecino] = g_candidato
                f_costo = g_candidato + manhattan(vecino, destino)
                heappush(lista_abierta, (f_costo, vecino))

            yield ("vecino", vecino)


def manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos (a y b). 
    Es la suma de las diferencias absolutas de sus coordenadas.
    Sirve como heurística para estimar la distancia restante hasta el destino.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


init()
