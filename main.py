import pygame
import ia
import elementos

pygame.init()
CELL_SIZE = 10
BOARD_WIDTH = 640
BOAR_HEIGHT = 480


def aCoordenadasXY(PosX, PosY, step):
    return int(PosX/step), int(PosY/step)


def aCoordenadasAbsolutas(posx, posy, step):
    return posx * step, posy * step


def init():
    screen = pygame.display.set_mode(
        (BOARD_WIDTH, BOAR_HEIGHT))
    clock = pygame.time.Clock()
    SNAKE_COLOR = (255, 0, 0)
    SNAKE_DEATH_COLOR = (238, 130, 238)
    WALL_COLOR = (255, 255, 0)
    TAIL_COLOR = (255, 255, 0)
    FOOD_COLOR = (0, 255, 0)
    BG_COLOR = (0, 0, 0)

    x = CELL_SIZE * 2
    y = CELL_SIZE * 2

    comida = elementos.Comida(color=FOOD_COLOR, cellSize=CELL_SIZE)
    muro = elementos.Muro(screen, color=WALL_COLOR)

    snake = elementos.Humano(
        colorCabeza=SNAKE_COLOR, 
        colorCuerpo=TAIL_COLOR, 
        x=x, y=y,
        cellSize = CELL_SIZE)

    comida.reaparecer(screen)

    salir = False
    gameover = False
    while not gameover:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                salir = True
                continue

        snake.tick()

        screen.fill(BG_COLOR)  # Fill the display with a solid color

        rectSnake = snake.getRect()
        # si hay comida genero nueva comida
        if rectSnake.colliderect(comida.getRect()):
            snake.alimentar()
            comida.reaparecer(screen)

        muro.dibujar(screen)
        snake.dibujar(screen)
        comida.dibujar(screen)

        if muro.hayColision(snake) or snake.hayColisionConCuerpo():
            gameover = True

        pygame.display.flip()
        clock.tick(5)

    # mostramos mensaje de game over
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
                continue
        screen.fill(BG_COLOR)  # Fill the display with a solid color
        pygame.draw.rect(screen, SNAKE_DEATH_COLOR,
                         (screen.get_width() / 2, screen.get_height() / 2, CELL_SIZE * 2, CELL_SIZE * 2))

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


def initIA():
    screen = pygame.display.set_mode((BOARD_WIDTH, BOAR_HEIGHT))
    clock = pygame.time.Clock()
    SNAKE_COLOR = (255, 0, 0)
    SNAKE_DEATH_COLOR = (238, 130, 238)
    WALL_COLOR = (255, 255, 0)
    TAIL_COLOR = (255, 102, 102)
    FOOD_COLOR = (0, 255, 0)

    BG_COLOR = (0, 0, 0)
    PLAYER_WIDTH, PLAYER_HEIGHT = 10, 10
    WALL_WIDTH = PLAYER_WIDTH * 2
    WALL_HEIGHT = PLAYER_HEIGHT * 2
    STEP = PLAYER_WIDTH
    x, y = WALL_WIDTH, WALL_HEIGHT

    cola = []
    comida = obtenerComidaRandom()
    start = aCoordenadasXY(x, y, STEP)
    goal = aCoordenadasXY(comida.x, comida.y, STEP)
    newStar = goal
    board_width, board_height = int(
        BOARD_WIDTH / PLAYER_WIDTH), int(BOAR_HEIGHT / PLAYER_HEIGHT)
    obstacles = {}
    path = ia.astar(start, goal, board_width, board_height, obstacles)

    print(f">>>>> path: {path} ")

    salir = False
    gameover = False
    while not gameover:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                salir = True
                continue

        if len(path) > 0:
            xx, yy = path.pop(0)
            xCola, yCola = aCoordenadasAbsolutas(xx, yy, STEP)
            cola.append(pygame.Rect(xCola, yCola, STEP, STEP))

            snake = pygame.Rect(xx * PLAYER_WIDTH, yy *
                                PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

            if snake.colliderect(comida):
                print(f"comiendo, nuevo largo de snake: {len(cola)}")
                comida = obtenerComidaRandom(cola)
            else:  # sino hay comida, elimino el ultimo elemento de la cola
                cola.pop(0)
        else:

            newGoal = aCoordenadasXY(comida.x, comida.y, STEP)

            path = ia.astar(newStar, newGoal, board_width,
                            board_height, obstacles)
            print(f">>>>> path: {path} ")

        screen.fill(BG_COLOR)  # Fill the display with a solid color

        initStage(WALL_WIDTH, WALL_HEIGHT, screen, WALL_COLOR)
        dibujarCola(cola, TAIL_COLOR, PLAYER_HEIGHT, screen)

        pygame.draw.rect(screen, SNAKE_COLOR, snake)
        pygame.draw.rect(screen, FOOD_COLOR, comida)

        # if (wallCollision(x, y, WALL_WIDTH, WALL_HEIGHT, screen)) or hayColisionCola(snake, cola):
        #   gameover = True

        pygame.display.flip()
        clock.tick(5)

    # mostramos mensaje de game over
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
                continue
        screen.fill(BG_COLOR)  # Fill the display with a solid color
        pygame.draw.rect(screen, SNAKE_DEATH_COLOR,
                         (screen.get_width() / 2, screen.get_height() / 2, PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))

        pygame.display.flip()
        clock.tick(1)

    pygame.quit()


init()
# initIA()
