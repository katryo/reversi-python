from copy import deepcopy
from random import randint
PLAYER_O = 0
PLAYER_X = 1
BLANK = '-'
STONE_O = 'O'
STONE_X = 'X'
CONTINUE = 0
END = 1
INVALID = 2


class Game:
    def __init__(self, x_is_computer=True):
        self.board = [[BLANK] * 8 for _ in range(8)]
        self.board[3][3] = STONE_O
        self.board[4][4] = STONE_O
        self.board[3][4] = STONE_X
        self.board[4][3] = STONE_X
        self.current_player = PLAYER_O
        self.move_count = 4
        self.x_is_computer = x_is_computer

    def _off_board(self, row, col):
        return row < 0 or row > 7 or col < 0 or col > 7

    def _on_board(self, row, col):
        return not self._off_board(row, col)

    def _oponent_stone(self):
        if self.current_player == PLAYER_X:
            return STONE_O
        return STONE_X

    def _players_stone(self):
        if self.current_player == PLAYER_X:
            return STONE_X
        return STONE_O

    def _put_stone_flip(self, row, col):
        self.board[row][col] = self._players_stone()
        total = 0
        for rd, cd in ((1, 0), (-1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            total += self._put_stone_flip_direction(row, rd, col, cd)
        return total

    def _put_stone_flip_direction(self, row, rd, col, cd):
        r = row + rd
        c = col + cd
        total = 0
        while self._on_board(r, c) and self.board[r][c] == self._oponent_stone():
            total += 1
            self.board[r][c] = self._players_stone()
            r += rd
            c += cd
        if self._on_board(r, c) and self.board[r][c] == self._players_stone():
            return total
        return 0

    def _can_flip_stone(self, row, col):
        prev_board = deepcopy(self.board)
        stone_flipped = self._put_stone_flip(row, col)

        self.board = prev_board
        return stone_flipped > 0

    def _play_move(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return INVALID
        if self.board[row][col] != BLANK:
            return INVALID

        prev_board = deepcopy(self.board)
        stone_flipped = self._put_stone_flip(row, col)
        if stone_flipped == 0:
            self.board = prev_board
            return INVALID
        self.move_count += 1

        if self.move_count == 8 * 8:
            return END

        s = set()
        for row in self.board:
            for cell in row:
                s.add(cell)
        if len(s) == 2:
            return END
        else:
            return CONTINUE

    def _show_board(self):
        for row in self.board:
            print(''.join(row))

    def _show_result(self):
        self._show_board()
        o = 0
        x = 0
        for row in self.board:
            for cell in row:
                if cell == STONE_O:
                    o += 1
                else:
                    x += 1
        print("O:{}, X:{}".format(o, x))
        if o > x:
            print("O won!")
        elif o == x:
            print("Tie")
        else:
            print("X won!")

    def _change_turn(self):
        if self.current_player == PLAYER_O:
            self.current_player = PLAYER_X
        else:
            self.current_player = PLAYER_O

    def start(self):
        passed = False
        while True:
            availables = []
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] == BLANK and self._can_flip_stone(i, j):
                        availables.append((i, j))

            for counter, (i, j) in enumerate(availables):
                self.board[i][j] = chr(ord('a')+counter)

            self._show_board()
            for i, j in availables:
                self.board[i][j] = BLANK

            if availables:
                passed = False
            else:
                if passed:
                    print("End.")
                    self._show_result()
                    return
                print("Pass")
                passed = True
                self._change_turn()
                continue

            if not self.x_is_computer or self.current_player == PLAYER_O:
                line = input().strip()
                try:
                    num = ord(line)-ord('a')
                except:
                    print("Invalid input")
                    continue
                if num < 0 or len(availables)-1 < num:
                    print("Invalid input")
                    continue
                row, col = availables[num]
            else:
                num = randint(0, len(availables)-1)
                row, col = availables[num]
            result = self._play_move(row, col)
            if result == INVALID:
                print("Invalid move")
                continue
            if result == END:
                self._show_result()
                return
            self._change_turn()


if __name__ == '__main__':
    game = Game()
    # print(game._can_flip_stone(4, 2))
    game.start()
