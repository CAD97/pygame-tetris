from typing import List
from pygame import Color
import random


class Tetris:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height + 2)]
        self.upcoming = TetrisPiece.all
        random.shuffle(self.upcoming)
        self.floating = TetrisPiece.Null
        self.floating_pos = (0, 0)
        self.lock()
        assert self._consistent()

    def __str__(self) -> str:
        grid = list(map(lambda line: list(map(lambda block: '[]' if block else '  ', line)), self.grid))
        y, x = self.floating_pos
        for dy in range(self.floating.height):
            for dx in range(self.floating.width):
                if self.floating.shape[dy][dx]:
                    grid[y + dy][x + dx] = '{}'
        return '\n'.join(map(''.join, grid))

    def __repr__(self) -> str:
        return f'Tetris({self.grid})'

    def left_shift(self) -> bool:
        """Shift the floating piece one position left.
           Returns whether the shift was successful."""
        y, x = self.floating_pos
        self.floating_pos = (y, x - 1)
        if self._consistent():
            return True
        else:
            self.floating_pos = (y, x)
            return False

    def right_shift(self) -> bool:
        """Shift the floating piece one position right.
           Returns whether the shift was successful."""
        assert self._consistent()
        y, x = self.floating_pos
        self.floating_pos = (y, x + 1)
        if self._consistent():
            return True
        else:
            self.floating_pos = (y, x)
            return False

    def soft_drop(self) -> bool:
        """Shift the floating piece one position down.
           Returns whether the shift was successful."""
        assert self._consistent()
        y, x = self.floating_pos
        self.floating_pos = (y + 1, x)
        if self._consistent():
            return True
        else:
            self.floating_pos = (y, x)
            return False

    def hard_drop(self):
        """Shift the floating piece all the way down.
           Does not lock the piece in place."""
        assert self._consistent()
        while self.soft_drop():
            pass
        assert self._consistent()

    def lock(self) -> bool:
        """Lock the floating piece in place and spawn the next floating piece.
           Returns if the game is still valid and can continue."""
        assert self._consistent()
        y, x = self.floating_pos
        for dy in range(self.floating.height):
            for dx in range(self.floating.width):
                if self.floating.shape[dy][dx]:
                    self.grid[y + dy][x + dx] = self.floating.shape[dy][dx]
        self.floating_pos = (0, 4)
        self.floating = self.upcoming.pop()
        if not self.upcoming:
            self.upcoming = TetrisPiece.all
            random.shuffle(self.upcoming)
        return self._consistent()

    # validity checks
    def _consistent(self) -> bool:
        return self._floating_inbounds() and not self._floating_overlap()

    def _floating_inbounds(self) -> bool:
        y, x = self.floating_pos
        for dy in range(self.floating.height):
            for dx in range(self.floating.width):
                if self.floating.shape[dy][dx]:
                    if not (0 <= (x + dx) < self.width and 0 <= (y + dy) < (self.height + 2)):
                        return False
        return True

    def _floating_overlap(self) -> bool:
        y, x = self.floating_pos
        for dy in range(self.floating.height):
            for dx in range(self.floating.width):
                if self.floating.shape[dy][dx] and self.grid[y + dy][x + dx]:
                    return True
        return False


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
TetrisPiece.Null = TetrisPiece([[]])

del i, j, l, o, s, t, z, N

TetrisPiece.all = [TetrisPiece.I, TetrisPiece.J, TetrisPiece.L,
                   TetrisPiece.O, TetrisPiece.S,
                   TetrisPiece.T, TetrisPiece.Z]
