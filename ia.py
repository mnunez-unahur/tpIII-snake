from heapq import heappush, heappop


def manhattan(a, b):
    """Calcula la distancia Manhattan entre dos puntos (a y b). 
    Es la suma de las diferencias absolutas de sus coordenadas.
    Sirve como heurística para estimar la distancia restante hasta el destino.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# En el algoritmo A*, cada nodo tiene un costo total f(n):
#   f(n) = g(n) + h(n)
# donde:
#   g(n): costo real para llegar al nodo n desde el inicio.
#   h(n): costo estimado (heurístico) desde n hasta el destino.
#   f(n): prioridad total usada para decidir qué nodo explorar primero.

def astar(inicio, destino, grafo, board_width, board_height, obstaculos):
    """
    Implementación del algoritmo A* para encontrar el camino más corto entre 'inicio' y 'destino' 
    en un grafo o grilla. Usa la heurística de Manhattan.

    Parámetros:
        inicio (tuple): coordenadas del nodo inicial.
        destino (tuple): coordenadas del nodo final.
        grafo (networkx.Graph): grafo que define la conectividad entre nodos.
        board_width, board_height (int): tamaño de la grilla (solo relevante si se usa la versión de grilla).
        obstaculos (set): conjunto de nodos bloqueados o no transitables.

    Retorna:
        list: lista ordenada de nodos que conforman el camino desde inicio a destino.
              Retorna None si no se encuentra camino posible.
    """

    # Cola de prioridad (heap) que almacena nodos pendientes de explorar.
    # Cada elemento es una tupla (f_score, nodo), y siempre se explora el nodo con menor f_score.
    lista_abierta = []
    heappush(lista_abierta, (0, inicio))

    # Diccionario para reconstruir el camino una vez alcanzado el destino.
    viene_de = {}

    # Costo acumulado más bajo conocido hasta cada nodo.
    # Comienza con el nodo inicial, cuyo costo de llegada (g) es 0.
    g_costo = {inicio: 0}

    while lista_abierta:
        # Se extrae el nodo con menor f(n) de la cola de prioridad.
        _, nodo_actual = heappop(lista_abierta)

        # Si alcanzamos el destino, reconstruimos el camino recorriendo "viene_de".
        if nodo_actual == destino:
            ruta = []
            while nodo_actual in viene_de:
                ruta.append(nodo_actual)
                nodo_actual = viene_de[nodo_actual]
            ruta.append(inicio)
            ruta.reverse()
            return ruta

        # --- EXPLORACIÓN DE VECINOS (versión con grafo) ---
        # print(f"Nodo actual: {nodo_actual} Vecinos: {[n for n in grafo.neighbors(nodo_actual)]}")

        for vecino in grafo.neighbors(nodo_actual):
            # Si el vecino es un obstáculo (y no es el destino), se salta.
            if vecino in obstaculos and vecino != destino:
                continue

            # Costo tentativo: costo acumulado para llegar hasta el vecino
            # pasando por el nodo actual. Aquí se asume que moverse cuesta 1 unidad.
            g_candidato = g_costo[nodo_actual] + 1

            # Si el nuevo costo es mejor (más bajo) que el registrado previamente,
            # actualizamos el costo y la relación "viene_de".
            if g_candidato < g_costo.get(vecino, float('inf')):
                viene_de[vecino] = nodo_actual
                g_costo[vecino] = g_candidato

                # f(n) = g(n) + h(n)
                # Se calcula la prioridad combinando el costo real y la heurística.
                f_costo = g_candidato + manhattan(vecino, destino)

                # Se agrega el vecino a la lista abierta (cola de prioridad)
                # para ser explorado más adelante.
                heappush(lista_abierta, (f_costo, vecino))

        # --- VERSIÓN ALTERNATIVA (si se trabaja con grilla en lugar de grafo) ---
        # x, y = nodo_actual
        # vecinos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        #
        # for nx, ny in vecinos:
        #     if not (0 <= nx < board_width and 0 <= ny < board_height):
        #         continue
        #
        #     if (nx, ny) in obstaculos and (nx, ny) != destino:
        #         continue
        #
        #     g_candidato = g_costo[nodo_actual] + 1
        #     if g_candidato < g_costo.get((nx, ny), float('inf')):
        #         viene_de[(nx, ny)] = nodo_actual
        #         g_costo[(nx, ny)] = g_candidato
        #         f_costo = g_candidato + manhattan((nx, ny), destino)
        #         heappush(lista_abierta, (f_costo, (nx, ny)))

    # Si la lista abierta se vacía sin haber alcanzado el destino, no hay camino posible.
    return None
