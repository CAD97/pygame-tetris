import pygame, sys


def main():
    pygame.init()

    size = width, height = 320, 240
    screen = pygame.display.set_mode(size)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


if __name__ == '__main__':
    main()
