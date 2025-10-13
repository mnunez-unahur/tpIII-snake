import pygame
import random
import ia
import elementos

pygame.init()


def movePlayer(x, y, cellSize, dir, cola=[], alargarCola=False):
    cola.append(pygame.Rect(x, y, cellSize, cellSize))
    if dir == DIR_LEFT:
        x -= cellSize
    if dir == DIR_RIGHT:
        x += cellSize
    if dir == DIR_UP:
        y -= cellSize
    if dir == DIR_DOWN:
        y += cellSize
    return x, y, cola



DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
DIR_UP = 'UP'
DIR_DOWN = 'DOWN'
CELL_SIZE = 10
BOARD_WIDTH = 640
BOAR_HEIGHT = 480


def getDirection():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        return DIR_LEFT
    if keys[pygame.K_RIGHT]:
        return DIR_RIGHT
    if keys[pygame.K_UP]:
        return DIR_UP
    if keys[pygame.K_DOWN]:
        return DIR_DOWN

# Dibuja los bordes


def initStage(width, height, screen, color):
    pygame.draw.rect(screen, color,
                     (0, 0, screen.get_width(), height))
    pygame.draw.rect(screen, color, (screen.get_width(
    ) - width, 0, screen.get_width() - width, screen.get_height()))
    pygame.draw.rect(screen, color, (0, screen.get_height(
    ) - height, screen.get_width(), height))
    pygame.draw.rect(screen, color,
                     (0, 0, width, screen.get_height()))

# Chequea la colision con los muros


def wallCollision(x, y, wall_width, wall_height, screen):
    if x < wall_width:
        return True
    elif x > screen.get_width() - wall_width:
        return True
    elif y < wall_height:
        return True
    elif y > screen.get_height() - wall_height:
        return True
    else:
        return False


def aCoordenadasXY(PosX, PosY, step):
    return int(PosX/step), int(PosY/step)


def aCoordenadasAbsolutas(posx, posy, step):
    return posx * step, posy * step


def obtenerComidaRandom(cola=[]):
    randomX = random.randint(
        20, int(BOARD_WIDTH/CELL_SIZE)-CELL_SIZE*2) * CELL_SIZE
    randomY = random.randint(
        20, int(BOAR_HEIGHT/CELL_SIZE)-CELL_SIZE*2) * CELL_SIZE

    # TODO: hacer que no aparezca sobre la cola

    return pygame.Rect(randomX, randomY, CELL_SIZE, CELL_SIZE)


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

    WALL_WIDTH = CELL_SIZE * 2
    WALL_HEIGHT = CELL_SIZE * 2
    x, y = WALL_WIDTH, WALL_HEIGHT

    comida = obtenerComidaRandom()

    snake = elementos.Humano(
        colorCabeza=SNAKE_COLOR, 
        colorCuerpo=TAIL_COLOR, 
        x=x, y=y,
        cellSize = CELL_SIZE)

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

        rectSnake = snake.getRect()

        # si hay comida genero nueva comida
        if rectSnake.colliderect(comida):
            snake.alimentar()
            comida = obtenerComidaRandom(snake.cola)

        screen.fill(BG_COLOR)  # Fill the display with a solid color

        initStage(WALL_WIDTH, WALL_HEIGHT, screen, WALL_COLOR)
        snake.dibujar(screen)
        pygame.draw.rect(screen, FOOD_COLOR, comida)

        if (wallCollision(x, y, WALL_WIDTH, WALL_HEIGHT, screen)) or snake.hayColisionConCuerpo():
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
