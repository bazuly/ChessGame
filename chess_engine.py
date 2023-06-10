
class GameState():
    def __init__(self):
        # Better to use numpy for this, but who cares
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                               'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.White_to_move_first = True
        # move recording
        self.moveLog = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.check_mate = False
        self.stalemate = False # пат

    def make_move(self, move):
        if self.board[move.startrow][move.startcol] != '--':
            self.board[move.startrow][move.startcol] = '--'
            self.board[move.endrow][move.endcol] = move.piece_moved
            self.moveLog.append(move) # record move
            # easiest way to swap white to black
            self.White_to_move_first = not self.White_to_move_first
            # tracking king location
            if move.piece_moved == 'wK':
                self.white_king_location = [move.endrow, move.endcol]
            elif move.piece_moved == 'bK':
                self.black_king_location = [move.endrow, move.endcol]
            # promotion move, queen or knight !
            if move.pawn_promotion:
                self.board[move.endrow][move.endcol] = move.piece_moved[0] + 'Q'

    def undo_move(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startrow][move.startcol] = move.piece_moved
            self.board[move.endrow][move.endcol] = move.piece_captured
            self.White_to_move_first = not self.White_to_move_first
            # also tracking king location after undo move
            if move.piece_moved == 'wK':
                self.white_king_location = [move.startrow, move.startcol]
            if move.piece_moved == 'bK':
                self.black_king_location = [move.startrow, move.startcol]

    def get_valid_moves(self):
        moves = self.get_all_possible_moves()
        for i in range(len(moves)-1, -1, -1): # -1 -1 need to avoid bugs, starting from the last element
            self.make_move(moves[i]) # making move
            # we need to swap turns, cuz it will look on white king, when we are attacking black king
            # cuz self.make_move switch the turn
            self.White_to_move_first = not self.White_to_move_first
            if self.check():
                # remove from valid moves
                moves.remove(moves[i])
            self.White_to_move_first = not self.White_to_move_first
            self.undo_move()

        if len(moves) == 0: # checkmate or stalemate
            if self.check():
                self.check_mate = True
            else:
                self.stalemate = True

        else:
            self.check_mate = False
            self.stalemate = False

        return moves

    def check(self):
        # checking that out king attacked by enemy piece
        if self.White_to_move_first:
            return self.attacked_square(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.attacked_square(self.black_king_location[0], self.black_king_location[1])

    def attacked_square(self, row, column):
        self.White_to_move_first = not self.White_to_move_first # switching to the opponent's move
        opp_moves = self.get_all_possible_moves() # find opponent's move
        self.White_to_move_first = not self.White_to_move_first
        for move in opp_moves:
            if move.endrow == row and move.endcol == column: # find attacked square
                return True
        return False

    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)): # number of rows
            for column in range(len(self.board[row])): # number of columns in given row
                color_turn = self.board[row][column][0] # choose square and piece color from the square
                if (color_turn == 'w' and self.White_to_move_first) or \
                        (color_turn == 'b' and not self.White_to_move_first):
                    piece = self.board[row][column][1]
                    self.move_functions[piece](row, column, moves)
        return moves

    def get_pawn_moves(self, row, column, moves):
        if self.White_to_move_first:
            if self.board[row - 1][column] == '--':
                moves.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == '--':
                    moves.append(Move((row, column), (row - 2, column), self.board))
                # captures to the left
                if column - 1 >= 0: # cuz we can't capture piece outside the board
                    if self.board[row - 1][column - 1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))
                # captures to the right
                if column + 1 <= 7:
                    if self.board[row - 1][column + 1][0] == 'b':
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))
        else:
            if not self.White_to_move_first:
                if self.board[row + 1][column] == '--':
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    if row == 1 and self.board[row + 2][column] == '--':
                        moves.append(Move((row, column), (row + 2, column), self.board))
                    # captures to the left
                if column - 1 >= 0:
                    if self.board[row + 1][column - 1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
                if column + 1 <= 7:
                    if self.board[row + 1][column + 1][0] == 'w':
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row, column, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        if self.White_to_move_first:
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # piece on board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--': # valid move
                        moves.append(Move((row, column), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_col), self.board))
                        break
                    else: # if friendly piece on the square
                        break
                else: # if piece outside the board
                    break

    def get_bishop_moves(self, row, column, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = 'b' if self.White_to_move_first else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = column + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':  # valid move
                        moves.append(Move((row, column), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_col), self.board))
                        break
                    else:  # if friendly piece on the square
                        break
                else:  # if piece outside the board
                    break

    def get_knight_moves(self, row, column, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.White_to_move_first else 'b'
        for d in directions:
            end_row = row + d[0]
            end_col = column + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece != ally_color:
                    moves.append(Move((row, column), (end_row, end_col), self.board))

    def get_queen_moves(self, row, column, moves):
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        directions = ((-1, 0), (-1, 1), (-1, -1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1))
        ally_color = 'w' if self.White_to_move_first else 'b'
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = column + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece != ally_color:
                    moves.append(Move((row, column), (end_row, end_col), self.board))


class Move():
    ranks_to_rows = {'1': 7, "2": 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                        'e': 4, 'f': 5, 'g': 6, 'h': 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, startsq, endsq, board):
        self.startrow = startsq[0]
        self.startcol = startsq[1]
        self.endrow = endsq[0]
        self.endcol = endsq[1]
        self.piece_moved = board[self.startrow][self.startcol]
        self.piece_captured = board[self.endrow][self.endcol]
        self.pawn_promotion = False
        if (self.piece_moved == 'wp' and self.endrow == 0) or (self.piece_moved == 'bp' and self.endrow == 7):
            self.pawn_promotion = True
        self.moveID = self.startrow * 1000 + self.startcol * 100 + self.endrow * 10 + self.endcol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        else:
            return False

    def get_chess_notation(self):
        return self.get_Rank_file(self.startrow, self.startcol) + self.get_Rank_file(self.endrow, self.endcol)

    def get_Rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]

