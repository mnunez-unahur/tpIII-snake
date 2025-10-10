import pygame

pygame.init()


def controls(x, y, speed):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    return x, y


def initStage(width, height, screen, color):
    pygame.draw.rect(screen, color,
                     (0, 0, screen.get_width(), height))
    pygame.draw.rect(screen, color, (screen.get_width(
    ) - width, 0, screen.get_width() - width, screen.get_height()))
    pygame.draw.rect(screen, color, (0, screen.get_height(
    ) - height, screen.get_width(), height))
    pygame.draw.rect(screen, color,
                     (0, 0, width, screen.get_height()))


def init():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    SNAKE_COLOR = (255, 0, 0)
    WALL_COLOR = (255, 255, 0)
    BG_COLOR = (0, 0, 0)
    x, y = 0, 0
    width, height = 10, 10
    speed = 5

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        # Falta los limites en funcion del ancho de las paredes
        x, y = controls(x, y, speed)

        screen.fill(BG_COLOR)  # Fill the display with a solid color

        initStage(width, height, screen, WALL_COLOR)
        pygame.draw.rect(screen, SNAKE_COLOR, (x, y, width, height))

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(60)         # wait until next frame (at 60 FPS)


init()
