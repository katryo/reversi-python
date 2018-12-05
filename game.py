PLAYER_O = 0
PLAYER_X = 1
BLANK = '-'
STONE_O = 'O'
STONE_X = 'X'
CONTINUE = 0
END = 1
INVALID = 2


class Game:
    def __init__(self):
        self.board = [[BLANK] * 8 for _ in range(8)]
        self.board[3][3] = STONE_O
        self.board[4][4] = STONE_O
        self.board[3][4] = STONE_X
        self.board[4][3] = STONE_X
        self.current_player = PLAYER_O
        self.move_count = 4

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

    def _can_flip_move(self, row, row_diff, col, col_diff):
        if not self._on_board(row + row_diff, col+col_diff):
            return False
        if self.board[row+row_diff][col+col_diff] != self._oponent_stone():
            return False
        r = row+row_diff
        c = col+col_diff
        while self._on_board(r, c) and self.board[r][c] == self._oponent_stone():
            r += row_diff
            c += col_diff
        if self._on_board(r, c) and self.board[r][c] == self._players_stone():
            return True
        return False

    def _can_flip_stone(self, row, col):
        return self._can_flip_move(row, -1, col, 0) or \
               self._can_flip_move(row, 1, col, 0) or \
               self._can_flip_move(row, 0, col, 1) or \
               self._can_flip_move(row, 0, col, -1)

    def _put_stone_flip(self, row, col):
        self.board[row][col] = self._players_stone()
        if self._can_flip_move(row, -1, col, 0):
            self._put_stone_flip_direction(row, -1, col, 0)
        if self._can_flip_move(row, 1, col, 0):
            self._put_stone_flip_direction(row, 1, col, 0)
        if self._can_flip_move(row, 0, col, -1):
            self._put_stone_flip_direction(row, 0, col, -1)
        if self._can_flip_move(row, 0, col, 1):
            self._put_stone_flip_direction(row, 0, col, 1)

    def _put_stone_flip_direction(self, row, rd, col, cd):
        r = row + rd
        c = col + cd
        while self.board[r][c] != self._players_stone():
            self.board[r][c] = self._players_stone()
            r += rd
            c += cd

    def _play_move(self, row, col):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return INVALID
        if self.board[row][col] != BLANK:
            return INVALID

        if not self._can_flip_stone(row, col):
            return INVALID

        self._put_stone_flip(row, col)
        self.move_count += 1

        if self.move_count == 8 * 8:
            return END
        else:
            return CONTINUE

    def _show_board(self):
        for row in self.board:
            print(''.join(row))

    def _show_result(self):
        assert self.move_count == 8 * 8
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

    def start(self):
        while True:
            self._show_board()
            line = input().strip()
            try:
                row, col = [int(x) for x in line.split(' ')]
            except:
                print("Invalid input")
                continue
            result = self._play_move(row, col)
            if result == INVALID:
                print("Invalid move")
                continue
            if result == END:
                self._show_result()
            if self.current_player == PLAYER_O:
                self.current_player = PLAYER_X
            else:
                self.current_player = PLAYER_O


if __name__ == '__main__':
    game = Game()
    # print(game._can_flip_stone(4, 2))
    game.start()