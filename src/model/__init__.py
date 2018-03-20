from typing import List
from pygame import Color
import random


class Tetris:
    def __init__(self):
        self.grid = [[None for _ in range(10)] for _ in range(22)]
        self.upcoming = TetrisPiece.all
        random.shuffle(self.upcoming)
        self.floating = self.upcoming.pop()
        self.floating_pos = (0, 4)

    def __str__(self):
        grid = list(map(lambda line: list(map(lambda block: '[]' if block else '  ', line)), self.grid))
        y, x = self.floating_pos
        for dy in range(self.floating.height):
            for dx in range(self.floating.width):
                if self.floating.shape[dy][dx]:
                    assert grid[y + dy][x + dx] == '  '
                    grid[y + dy][x + dx] = '{}'
        return '\n'.join(map(''.join, grid))

    def __repr__(self):
        return f'Tetris({self.grid})'


class TetrisPiece:
    def __init__(self, shape: List[List[Color]]):
        self.shape = shape
        self.height = len(shape)
        self.width = len(shape[0])
        for row in shape:
            assert len(row) == self.width

    def __str__(self):
        return '\n'.join(map(lambda line: ''.join(map(lambda block: '[]' if block else '  ', line)), self.shape))

    def __repr__(self):
        return f'TetrisPiece({self.shape})'


i = Color('cyan')
j = Color('blue')
l = Color('orange')
o = Color('yellow')
s = Color('green')
t = Color('purple')
z = Color('red')
N = None

TetrisPiece.I = TetrisPiece([[N, N, N, N],
                             [i, i, i, i],
                             [N, N, N, N],
                             [N, N, N, N]])
TetrisPiece.J = TetrisPiece([[j, N, N],
                             [j, j, j],
                             [N, N, N]])
TetrisPiece.L = TetrisPiece([[N, N, l],
                             [l, l, l],
                             [N, N, N]])
TetrisPiece.O = TetrisPiece([[N, N, N, N],
                             [N, o, o, N],
                             [N, o, o, N],
                             [N, N, N, N]])
TetrisPiece.S = TetrisPiece([[N, s, s],
                             [s, s, N],
                             [N, N, N]])
TetrisPiece.T = TetrisPiece([[N, t, N],
                             [t, t, t],
                             [N, N, N]])
TetrisPiece.Z = TetrisPiece([[z, z, N],
                             [N, z, z],
                             [N, N, N]])

del i, j, l, o, s, t, z, N

TetrisPiece.all = [TetrisPiece.I, TetrisPiece.J, TetrisPiece.L,
                   TetrisPiece.O, TetrisPiece.S,
                   TetrisPiece.T, TetrisPiece.Z]
