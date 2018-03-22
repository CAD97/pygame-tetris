from collections import deque
from typing import List, Tuple, Deque, Optional
from pygame import Color
import random


class Tetris:
    width: int
    height: int
    grid: List[List[Optional[Color]]]
    upcoming: List['TetrisPiece']
    floating: 'TetrisPiece'
    floating_pos: Tuple[int, int]

    def __init__(self):
        self.width = 10
        self.height = 20
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height + 2)]
        self.upcoming = list(TetrisPiece.all)
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
        return '\n'.join(map(lambda it: '|' + ''.join(it) + '|', grid))

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
        self.floating = self.upcoming.pop().cloned()
        if not self.upcoming:
            self.upcoming = list(TetrisPiece.all)
            random.shuffle(self.upcoming)
        return self._consistent()

    def clear(self):
        assert self._consistent()
        for row_idx in range(len(self.grid)):
            if all(self.grid[row_idx]):
                self.grid = [[None for _ in range(self.width)]] + self.grid[:row_idx] + self.grid[row_idx+1:]
                assert self._consistent()

    def rotate_clockwise(self) -> bool:
        assert self._consistent()
        success = self._rotate_clockwise()
        assert self._consistent()
        return success

    def _rotate_clockwise(self) -> bool:
        self.floating.rotate_clockwise()
        for kick in self.floating.kick_clockwise[-1]:
            self.floating_pos = (self.floating_pos[0] + kick[0], self.floating_pos[1] + kick[1])
            if self._consistent():
                return True
            else:
                self.floating_pos = (self.floating_pos[0] - kick[0], self.floating_pos[1] - kick[1])
        self._rotate_counterclockwise()
        return False

    def rotate_counterclockwise(self) -> bool:
        assert self._consistent()
        success = self._rotate_counterclockwise()
        assert self._consistent()
        return success

    def _rotate_counterclockwise(self) -> bool:
        self.floating.rotate_counterclockwise()
        for kick in self.floating.kick_counterclockwise[-1]:
            self.floating_pos = (self.floating_pos[0] + kick[0], self.floating_pos[1] + kick[1])
            if self._consistent():
                return True
            else:
                self.floating_pos = (self.floating_pos[0] - kick[0], self.floating_pos[1] - kick[1])
        self._rotate_clockwise()
        return False

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
    shape: List[List[Color]]
    height: int
    width: int
    kick_clockwise: Deque[List[Tuple[int, int]]]
    kick_counterclockwise: Deque[List[Tuple[int, int]]]

    def __init__(
            self,
            shape: List[List[Color]],
            kick_clockwise=None,
            kick_counterclockwise=None
    ):
        if kick_clockwise is None:
            kick_clockwise = deque([[(0, 0)]])
        if kick_counterclockwise is None:
            kick_counterclockwise = deque([[(0, 0)]])

        self.shape = shape
        self.height = len(shape)
        self.width = len(shape[0])
        self.kick_clockwise = kick_clockwise
        self.kick_counterclockwise = kick_counterclockwise

        for row in shape:
            assert len(row) == self.width

    def __str__(self):
        return '\n'.join(map(lambda line: ''.join(map(lambda block: '[]' if block else '  ', line)), self.shape))

    def __repr__(self):
        return f'TetrisPiece({self.shape})'

    def cloned(self) -> 'TetrisPiece':
        return TetrisPiece(list(self.shape), deque(self.kick_clockwise), deque(self.kick_counterclockwise))

    def rotate_clockwise(self):
        self.kick_clockwise.rotate(-1)
        self.kick_counterclockwise.rotate(1)
        self.shape = list(zip(*self.shape[::-1]))

    def rotate_counterclockwise(self):
        self.kick_clockwise.rotate(1)
        self.kick_counterclockwise.rotate(-1)
        self.shape = list(reversed(list(zip(*self.shape))))


i = Color('cyan')
j = Color('blue')
l = Color('orange')
o = Color('yellow')
s = Color('green')
t = Color('purple')
z = Color('red')
N = None

# Arika SRS
i_kicks = (
    deque([
        [(0,0),(0,-2),(0,+1),(-2,+1),(+1,-2)],  # 0->R
        [(0,0),(0,-1),(0,+2),(-2,-1),(+1,+2)],  # R->2
        [(0,0),(0,+2),(0,-1),(-1,+2),(+1,-1)],  # 2->L
        [(0,0),(0,-2),(0,+1),(-1,-2),(+2,+1)],  # L->0
    ]),
    deque([
        [(0,0),(0,+2),(0,-1),(-2,-1),(+1,+2)],  # 0->L
        [(0,0),(0,+1),(0,-2),(-2,+1),(+1,-2)],  # L->2
        [(0,0),(0,-2),(0,+1),(-1,-2),(+2,+1)],  # 2->R
        [(0,0),(0,+2),(0,-1),(-1,+2),(+2,-1)],  # R->0
    ]),
)

jlstz_kicks = (
    deque([
        [(0,0),(0,-1),(-1,-1),(+2,0),(+2,-1)],  # 0->R
        [(0,0),(0,+1),(+1,+1),(-2,0),(-2,+1)],  # R->2
        [(0,0),(0,+1),(-1,+1),(+2,0),(+2,-1)],  # 2->L
        [(0,0),(0,-1),(+1,-1),(-2,0),(-2,-1)],  # L->0
    ]),
    deque([
        [(0,0),(0,+1),(-1,+1),(+2,0),(+2,+1)],  # 0->L
        [(0,0),(0,-1),(+1,-1),(-2,0),(-2,-1)],  # L->2
        [(0,0),(0,-1),(-1,-1),(+2,0),(+2,-1)],  # 2->R
        [(0,0),(0,+1),(+1,+1),(+2,0),(+2,-1)],  # R->0
    ]),
)

TetrisPiece.I = TetrisPiece([[N, N, N, N],
                             [i, i, i, i],
                             [N, N, N, N],
                             [N, N, N, N]],
                            *i_kicks)
TetrisPiece.J = TetrisPiece([[j, N, N],
                             [j, j, j],
                             [N, N, N]],
                            *jlstz_kicks)
TetrisPiece.L = TetrisPiece([[N, N, l],
                             [l, l, l],
                             [N, N, N]],
                            *jlstz_kicks)
TetrisPiece.O = TetrisPiece([[N, N, N, N],
                             [N, o, o, N],
                             [N, o, o, N],
                             [N, N, N, N]])
TetrisPiece.S = TetrisPiece([[N, s, s],
                             [s, s, N],
                             [N, N, N]],
                            *jlstz_kicks)
TetrisPiece.T = TetrisPiece([[N, t, N],
                             [t, t, t],
                             [N, N, N]],
                            *jlstz_kicks)
TetrisPiece.Z = TetrisPiece([[z, z, N],
                             [N, z, z],
                             [N, N, N]],
                            *jlstz_kicks)
TetrisPiece.Null = TetrisPiece([[]])

del i, j, l, o, s, t, z, N, i_kicks, jlstz_kicks

TetrisPiece.all = [TetrisPiece.I, TetrisPiece.J, TetrisPiece.L,
                   TetrisPiece.O, TetrisPiece.S,
                   TetrisPiece.T, TetrisPiece.Z]
