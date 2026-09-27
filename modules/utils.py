import sys
import pygame


def showText(screen, text, color, font, x, y):
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def showLife(screen, num_life, color):
    font = pygame.font.SysFont('arial', 28)
    for i in range(num_life):
        position = [700 - 35 * i, 8]
        text = font.render('♥', True, (255, 0, 0))
        screen.blit(text, position)


def endInterface(screen, color, is_win):
    screen.fill(color)
    clock = pygame.time.Clock()

    if is_win:
        text = 'VICTORY'
    else:
        text = 'FAILURE'

    font = pygame.font.SysFont('arial', 30)
    text_render = font.render(text, 1, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.blit(text_render, (350, 300))
        clock.tick(60)
        pygame.display.update()