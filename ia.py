from heapq import heappush, heappop

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(inicio, destino, grafo, board_width, board_height, obstaculos):
    open_set = []
    heappush(open_set, (0, inicio))
    came_from = {}
    g_score = {inicio: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == destino:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(inicio)
            path.reverse()
            return path

        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

        for nx, ny in neighbors:
            if not (0 <= nx < board_width and 0 <= ny < board_height):
                continue
            # print(f"{(nx, ny)} in obstacles: {(nx, ny) in obstacles}")
            if (nx, ny) in obstaculos and (nx, ny) != destino:
                continue

            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get((nx, ny), float('inf')):
                came_from[(nx, ny)] = current
                g_score[(nx, ny)] = tentative_g
                f_score = tentative_g + manhattan((nx, ny), destino)
                heappush(open_set, (f_score, (nx, ny)))

    return None  # no se encontró camino

# Ejemplo de uso
""" start = (5, 5)
goal = (10, 5)
board_width, board_height = 20, 20
obstacles = {}  # partes del cuerpo o muros

path = astar(start, goal, board_width, board_height, obstacles)
print(path)
 """