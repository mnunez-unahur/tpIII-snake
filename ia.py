from heapq import heappush, heappop


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# f(n) = g(n) + h(n)
# f(n): A* Score 
# g(n): Costo para llegar a n  
# h(n): Costo estimado para ir de n al destino

def astar(inicio, destino, grafo, board_width, board_height, obstaculos):
    open_set = []   # cola de prioridad donde se guarda los nodos pendientes por explorar
    # Siempre se saca el nodo con menor f_score o sea mejor candidato

    heappush(open_set, (0, inicio))
    came_from = {}  # diccionario que guarda de donde vino cada nodo para poder reconstruir el camino final
    # lo que ya costó llegar hasta ahora (inicia guardando el costo acumulado 0)
    g_score = {inicio: 0}

    while open_set:
        _, current = heappop(open_set)  # se extrae el nodo con menor f_score
        if current == destino:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(inicio)
            path.reverse()
            return path
        # Implementacion con Grafo
        for vecino in grafo.neighbors(current):
            if vecino in obstaculos and vecino != destino:
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(vecino, float('inf')):
                came_from[vecino] = current
                g_score[vecino] = tentative_g
                f_score = tentative_g + manhattan(vecino, destino)
                heappush(open_set, (f_score, vecino))
        
        # Implementacion con Grilla
        # x, y = current
        # neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        
        # for nx, ny in neighbors:
        #     if not (0 <= nx < board_width and 0 <= ny < board_height):
        #         continue
            
        #     if (nx, ny) in obstaculos and (nx, ny) != destino:
        #         continue

        #     tentative_g = g_score[current] + 1
        #     if tentative_g < g_score.get((nx, ny), float('inf')):
        #         came_from[(nx, ny)] = current
        #         g_score[(nx, ny)] = tentative_g
        #         f_score = tentative_g + manhattan((nx, ny), destino)
        #         heappush(open_set, (f_score, (nx, ny)))

    return None  # no se encontró camino

