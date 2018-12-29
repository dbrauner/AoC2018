import sys

import pygame

pygame.init()

size = width, height = 1024, 968

speed = [2, 2]

black = 255, 255, 255

screen = pygame.display.set_mode(size, 0, 8)

x, y = 0, 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if x > width:
        x = 0
        y += 1
    if y > height:
        sys.exit()
    x += 1
    screen.fill(black)
    for i in range(y):
        for j in range(x):
            screen.set_at((i, j), (255, 0, 0))
    # screen.blit(ball, ballrect)
    # pygame.display.flip()
    pygame.display.update()
# modes = pygame.display.list_modes(16)

# pygame.display.set_mode(modes[0], pygame.FULLSCREEN, 16)

# >>> #need an 8-bit surface, nothing else will do
# >>> if pygame.display.mode_ok((800, 600), 0, 8) != 8:
# ...     print 'Can only work with an 8-bit display, sorry'
# ... else:
# ...     pygame.display.set_mode((800, 600), 0, 8)
# surface.set_at((x, y), color)
