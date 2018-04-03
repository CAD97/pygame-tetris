import pygame, sys
from model import Tetris
from pygame import Color, Rect


def main():
    pygame.init()
    tetris = Tetris()
    font = pygame.font.SysFont('Sans Serif', 30)

    BLOCK_SIZE = 20
    BLACK = Color('black')

    screen = pygame.display.set_mode((tetris.width * BLOCK_SIZE + 5 * BLOCK_SIZE, tetris.height * BLOCK_SIZE))
    screen.fill(BLACK)

    playfield = Rect(0, 0, tetris.width * BLOCK_SIZE, tetris.height * BLOCK_SIZE)
    screen.fill(Color('white'), Rect(tetris.width * BLOCK_SIZE, 0, BLOCK_SIZE, screen.get_height()))
    hold = Rect(playfield.width + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE * 4, BLOCK_SIZE * 4)
    nxt = Rect(playfield.width + BLOCK_SIZE, BLOCK_SIZE * 6, BLOCK_SIZE * 4, BLOCK_SIZE * 16)

    hold_txt = font.render('HOLD', False, Color('white'))
    screen.blit(hold_txt, (playfield.width + BLOCK_SIZE * 1.5, 0))
    nxt_txt = font.render('NEXT', False, Color('white'))
    screen.blit(nxt_txt, (playfield.width + BLOCK_SIZE * 1.7, BLOCK_SIZE * 5))

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

        # clear playfield
        screen.fill(BLACK, playfield)
        # locked pieces
        for row_idx in range(tetris.height):
            for col_idx in range(tetris.width):
                if tetris.grid[row_idx][col_idx]:
                    rect = Rect(col_idx * BLOCK_SIZE, row_idx * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    screen.fill(tetris.grid[row_idx][col_idx], rect)
        # floating
        y, x = tetris.floating_pos
        for dy in range(tetris.floating.height):
            for dx in range(tetris.floating.width):
                mx = x + dx
                my = y + dy
                if tetris.floating.shape[dy][dx]:
                    rect = Rect(mx * BLOCK_SIZE, my * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    screen.fill(tetris.floating.shape[dy][dx], rect)

        # hold
        screen.fill(BLACK, hold)
        if tetris.holding:
            y, x = 1, tetris.width + 1
            for dy in range(tetris.holding.height):
                for dx in range(tetris.holding.width):
                    mx = x + dx
                    my = y + dy
                    if tetris.holding.shape[dy][dx]:
                        rect = Rect(mx * BLOCK_SIZE, my * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        screen.fill(tetris.holding.shape[dy][dx], rect)
        # upcoming
        screen.fill(BLACK, nxt)
        y, x = 2, tetris.width + 1
        for idx in range(4):
            y += 4
            for dy in range(tetris.upcoming[idx].height):
                for dx in range(tetris.upcoming[idx].width):
                    mx = x + dx
                    my = y + dy
                    if tetris.upcoming[idx].shape[dy][dx]:
                        rect = Rect(mx * BLOCK_SIZE, my * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                        screen.fill(tetris.upcoming[idx].shape[dy][dx], rect)

        pygame.display.flip()


if __name__ == '__main__':
    main()
