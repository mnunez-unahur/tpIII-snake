import pygame

pygame.init()


def movePlayer(x, y, speed, dir):

    if dir == DIR_LEFT:
        x -= speed
    if dir == DIR_RIGHT:
        x += speed
    if dir == DIR_UP:
        y -= speed
    if dir == DIR_DOWN:
        y += speed
    return x, y


DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
DIR_UP = 'UP'
DIR_DOWN = 'DOWN'


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


def initStage(width, height, screen, color):
    pygame.draw.rect(screen, color,
                     (0, 0, screen.get_width(), height))
    pygame.draw.rect(screen, color, (screen.get_width(
    ) - width, 0, screen.get_width() - width, screen.get_height()))
    pygame.draw.rect(screen, color, (0, screen.get_height(
    ) - height, screen.get_width(), height))
    pygame.draw.rect(screen, color,
                     (0, 0, width, screen.get_height()))


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


def init():
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    SNAKE_COLOR = (255, 0, 0)
    SNAKE_DEATH_COLOR = (238, 130, 238)
    WALL_COLOR = (255, 255, 0)
    BG_COLOR = (0, 0, 0)
    PLAYER_WIDTH, PLAYER_HEIGHT = 10, 10
    WALL_WIDTH = PLAYER_WIDTH * 2
    WALL_HEIGHT = PLAYER_HEIGHT * 2
    SPEED = PLAYER_WIDTH
    x, y = WALL_WIDTH, WALL_HEIGHT

    LAST_DIR = DIR_RIGHT
    currentDir = None

    while True:
        # Process player inputs.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if getDirection() != None:
            LAST_DIR = getDirection()
            currentDir = getDirection()
        else:
            currentDir = LAST_DIR

        x, y = movePlayer(x, y, SPEED, currentDir)

        screen.fill(BG_COLOR)  # Fill the display with a solid color

        initStage(WALL_WIDTH, WALL_HEIGHT, screen, WALL_COLOR)

        if (wallCollision(x, y, WALL_WIDTH, WALL_HEIGHT, screen)):

            pygame.draw.rect(screen, SNAKE_DEATH_COLOR,
                             (screen.get_width() / 2, screen.get_height() / 2, PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))
        else:
            pygame.draw.rect(screen, SNAKE_COLOR,
                             (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))

        pygame.display.flip()  # Refresh on-screen display
        clock.tick(5)         # wait until next frame (at 60 FPS)


init()
