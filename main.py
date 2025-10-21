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

    # snake = elementos.Humano(
    #     screen,
    #     colorCabeza=SNAKE_COLOR, 
    #     colorCuerpo=TAIL_COLOR, 
    #     x=x, y=y,
    #     cellSize = CELL_SIZE)

    snake = elementos.IA(
        screen, comida,
        colorCabeza=SNAKE_COLOR, 
        colorCuerpo=TAIL_COLOR, 
        x=x, y=y,
        cellSize = CELL_SIZE)

    comida.reaparecer(screen, snake)

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

        muro.dibujar(screen)
        snake.dibujar(screen)
        comida.dibujar(screen)

        if muro.hayColision(snake) or snake.hayColision(snake):
            gameover = True

        # si hay comida genero nueva comida
        if rectSnake.colliderect(comida.getRect()):
            snake.alimentar()
            comida.reaparecer(screen, snake)

        pygame.display.flip()
        clock.tick(30)

    # mostramos mensaje de game over
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
                continue
        # screen.fill(BG_COLOR)  # Fill the display with a solid color
        pygame.draw.rect(screen, SNAKE_DEATH_COLOR,
                         (screen.get_width() / 2, screen.get_height() / 2, CELL_SIZE * 2, CELL_SIZE * 2))

        pygame.display.flip()
        clock.tick(30)

    print(f"Puntos Totales: {snake.puntos}")
    pygame.quit()


init()
# initIA()
