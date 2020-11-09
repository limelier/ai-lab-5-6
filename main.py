from math import inf
from copy import deepcopy
from enum import Enum


class Direction(Enum):
    N = -1, 0,
    NE = -1, 1,
    E = 0, 1,
    SE = 1, 1,
    S = 1, 0,
    SW = 1, -1,
    W = 0, -1,
    NW = -1, -1,


class State:
    def __init__(self, starting: int = 2):
        self.board = [
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 2, 2, 2]
        ]
        self.next = starting

    def _copy(self):
        state = State()
        state.board = deepcopy(self.board)
        state.next = self.next
        return state

    def is_final(self):
        """
        Return 0 for no winners, or 1/2 for that player winning.
        """
        if self.board[0] == [2, 2, 2, 2]:
            return 2
        elif self.board[3] == [1, 1, 1, 1]:
            return 1
        else:
            return 0

    def evaluate(self):
        """
        Return player 1's advantage as a number representing the sum of player 1's advancements minus the sum
        of player 2's advancements.

        If the number is positive, the position favors player 1. If it's negative, it favors player 2.
        """
        point_sum = 0
        for row_idx, row in enumerate(self.board):
            for item in row:
                if item == 1:
                    point_sum += row_idx
                elif item == 2:
                    point_sum -= (3 - row_idx)
        return point_sum

    @staticmethod
    def _valid_position(row, col):
        return 0 <= row <= 3 and 0 <= col <= 3

    def _move_piece(self, row, col, direction: Direction):
        new_row, new_col = row + direction.value[0], col + direction.value[1]
        if not self._valid_position(new_row, new_col):
            return None
        if self.board[row][col] != self.next:
            return None
        if self.board[new_row][new_col] != 0:
            return None
        new_state = self._copy()
        new_state.board[new_row][new_col] = self.board[row][col]
        new_state.board[row][col] = 0
        new_state.next = 3 - self.next
        return new_state

    def generate_all(self):
        new_states = {
            self._move_piece(row, col, direction)
            for row in range(0, 4)
            for col in range(0, 4)
            for direction in Direction
        }
        new_states.discard(None)

        return new_states

    def print(self):
        print('Next: {}'.format(self.next))
        for line in self.board:
            print(' '.join([str(pos) for pos in line]))
        print()

    def do_player_move(self):
        self.print()
        inp = input('Input a move (row, col, dir) (e.g. 0 2 NE)\n')
        row_str, col_str, dir_str = inp.split()
        try:
            row, col, direction = int(row_str), int(col_str), Direction[dir_str]
        except ValueError:
            print('Row/col is not number (did you mistype?)')
            return None
        except KeyError:
            print('Dir is not in {N, NE, E, SE, S, SW, W, NW}')
            return None
        state = self._move_piece(row, col, direction)
        if state is None:
            print('Move is invalid (out of bounds / over another piece?)')
        return state

    def do_ai_move(self):
        best = None
        alpha = -inf
        beta = inf

        for state in self.generate_all():
            value = state.search(alpha, beta, 3, maximize=False)
            if value > alpha:
                alpha = value
                best = state
        return best

    def search(self, alpha, beta, depth, maximize: bool):
        if depth == 0 or self.is_final():
            return self.evaluate()

        if maximize:
            for state in self.generate_all():
                value = state.search(alpha, beta, depth - 1, not maximize)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return alpha
        else:
            for state in self.generate_all():
                value = state.search(alpha, beta, depth - 1, not maximize)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return beta


def test():
    state = State()
    while not state.is_final():
        if state.next == 1:
            state = state.do_ai_move()
        else:
            next_state = state.do_player_move()
            while next_state is None:
                next_state = state.do_player_move()
            state = next_state
    state.print()


if __name__ == '__main__':
    test()
