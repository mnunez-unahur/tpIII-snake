import pygame
import juego

pygame.init()


def aCoordenadasXY(PosX, PosY, step):
    return int(PosX/step), int(PosY/step)


def aCoordenadasAbsolutas(posx, posy, step):
    return posx * step, posy * step


def init():
    CELL_SIZE = 10
    SNAKE_COLOR = (255, 0, 0)
    SNAKE_DEATH_COLOR = (238, 130, 238)
    WALL_COLOR = (255, 255, 0)
    TAIL_COLOR = (255, 255, 0)
    FOOD_COLOR = (0, 255, 0)
    BG_COLOR = (0, 0, 0)
    FPS = 10
    grabarImageCamino = False

    modo = input("""Quien Juega? H=Humano / I=IA:  """).lower()
    if modo != "h" and modo != "i":
        print("modo no soportado")
        return 
    elif modo == "i":
        i = int(input("""Generar grafo_camino.png: (1 = Si) """))
        if i == 1:
            grabarImageCamino = True



    tablero = juego.Tablero(64, 48, CELL_SIZE, BG_COLOR)
    clock = pygame.time.Clock()

    xInicial, yInicial = tablero.centro()
    
    comida = juego.Comida(tablero, color=FOOD_COLOR)
    muro = juego.Muro(tablero, color=WALL_COLOR)

    snake = None

    if modo == "h":
        snake = juego.Humano(
            tablero,
            colorCabeza=SNAKE_COLOR,
            colorCuerpo=TAIL_COLOR,
            x=xInicial, y=yInicial,
            )
    else:
        snake = juego.IA(
            tablero, comida,
            colorCabeza=SNAKE_COLOR,
            colorCuerpo=TAIL_COLOR,
            x=xInicial, y=yInicial,
            grabarImageCamino=grabarImageCamino, 
            )


    comida.reaparecer(snake)

    salir = False
    gameover = False
    while not gameover:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
                salir = True
                continue

        # doy control al jugador
        snake.tick()

        tablero.limpiar()
        muro.dibujar()
        snake.dibujar()
        comida.dibujar()

        # si colisiona con un muro o con si misma pierde
        if muro.hayColision(snake) or snake.hayColision(snake):
            gameover = True

        # detectamos si hay comida en la posición actual
        rectSnake = snake.getRect()
        if rectSnake.colliderect(comida.getRect()):
            snake.alimentar()
            comida.reaparecer(snake)

        pygame.display.flip()

        # aumenta la velocidad a medida que tiene mas puntos
        clock.tick(FPS+snake.puntos)

    # mostramos mensaje de game over
    while not salir:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
                continue

        pygame.draw.rect(tablero.pantalla, SNAKE_DEATH_COLOR,
                         (tablero.pantalla.get_width() / 2, tablero.pantalla.get_height() / 2, CELL_SIZE * 2, CELL_SIZE * 2))

        pygame.display.flip()
        clock.tick(FPS)

    print(f"Puntos Totales: {snake.puntos}")
    pygame.quit()


init()
