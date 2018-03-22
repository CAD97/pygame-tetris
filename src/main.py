import pygame, sys
from model import Tetris
from pygame import Color, Rect


def main():
    pygame.init()
    tetris = Tetris()
    BLOCK_SIZE = 20

    size = width, height = tetris.width * BLOCK_SIZE, tetris.height * BLOCK_SIZE
    screen = pygame.display.set_mode(size)

    background = Color('black')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                key = event.unicode
                if key == 'z':
                    tetris.rotate_counterclockwise()
                elif key == 'x':
                    tetris.rotate_clockwise()
                elif key == 'r':
                    tetris = Tetris()
                    continue
                elif key == ' ':
                    tetris.hold()
                elif key == '':
                    key = event.key
                    if key == 273:
                        tetris.hard_drop()
                        tetris.lock()
                        tetris.clear()
                    if key == 274:
                        if not tetris.soft_drop():
                            tetris.lock()
                            tetris.clear()
                    if key == 275:
                        tetris.right_shift()
                    if key == 276:
                        tetris.left_shift()

        screen.fill(background)
        for row_idx in range(tetris.height):
            for col_idx in range(tetris.width):
                if tetris.grid[row_idx][col_idx]:
                    rect = Rect(col_idx * BLOCK_SIZE, row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    screen.fill(tetris.grid[row_idx][col_idx], rect)
        y, x = tetris.floating_pos
        for dy in range(tetris.floating.height):
            for dx in range(tetris.floating.width):
                mx = x + dx
                my = y + dy
                if tetris.floating.shape[dy][dx]:
                    rect = Rect(mx * BLOCK_SIZE, my * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    screen.fill(tetris.floating.shape[dy][dx], rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
