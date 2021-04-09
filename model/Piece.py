import math
from model import Positions

material_weights = {
    'pawn': 1,
    'rook': 5,
    'knight': 3,
    'bishop': 3,
    'queen': 9,
    'king': math.inf  # hmm
}


class Piece:
    """
    Properties of a Piece:
        - Color: 'black' or 'white'
        - Kind: in ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        - Material weight: 1, 3, 5, 9, or king
        - has_moved -> needed for castling, en passant
        - rank, file -> location value
        - board -> reference to board object for calculating moves
    """

    def __init__(self, white, kind, x, y, board):
        self.white = white
        self.kind = kind
        self.material_weight = material_weights[kind]
        self.has_moved = False
        self.rank, self.file = x, y
        self.board = board

    def copy(self):
        return Piece(self.white, self.kind, self.rank, self.file, self.board)

    def piece_to_fen_notation(self):
        kind_to_fen = {
            'pawn': 'p',
            'rook': 'r',
            'knight': 'n',
            'bishop': 'b',
            'queen': 'q',
            'king': 'k'
        }
        kind = kind_to_fen[self.kind]
        if self.white:
            kind = str.upper(kind)
        return kind

    def __str__(self):
        return self.piece_to_fen_notation()

    def legal_moves(self):
        '''
        A legal move satisfies these conditions:
        1 - the move obeys the directional ability of the piece. pawns move forward, bishops diagonally,
        rooks horizontally and vertically, queens both, and knights hop.
        2 - the destination square must not be occupied by a piece of the same color
        3 - moving the piece does not put your own king in check (ie, it's pinned)
            - note, this isn't that straightforward to build logic for, so we ignore for now. TODO
        4 - the destination square is not out of bounds of the dimensions of the board
        '''

        # first generate possible moves
        possible_moves = self.possible_moves()
        print('possible_moves:', possible_moves)

        legal_moves = self.truncate_possible_moves(possible_moves)

        return legal_moves

    def move_unoccupied_by_same_color(self, move):
        (rank, file) = move

        # if piece occupies square
        if self.board.is_occupied(rank, file):
            return self.board.piece_at_internal(rank, file).white ^ self.white
        else:
            return True

    def enemy_at(self, rank, file):
        if self.board.is_occupied(rank, file):
            return self.board.piece_at_internal(rank, file).white ^ self.white
        else:
            return False

    def friendly_at(self, rank, file):
        if self.board.is_occupied(rank, file):
            return not self.board.piece_at_internal(rank, file).white ^ self.white
        else:
            return False

    '''
        Possible Moves returns a list of lists. Each list is a vector of moves, so the return value is
        a list of all moves in all directions.
        This will then be filtered to truncate each list once a piece is discovered in that direction.
        (Pawns are an exception)
    '''

    """
        This method is implemented by the subclass.
    """

    def possible_moves(self):
        pass

    def truncate_possible_moves(self, possible_moves):
        truncated_all_moves = list()
        for directional_moves in possible_moves:
            trunc_directional_moves = list()
            for (rank, file) in directional_moves:
                trunc_directional_moves.append((rank, file))
                print('evaluating rank and file of', rank, file)
                if self.board.is_occupied(rank, file):
                    break
            if len(trunc_directional_moves):
                truncated_all_moves.append(trunc_directional_moves)
        flattened = [move for direction in truncated_all_moves for move in direction]
        print('flattened is', flattened)
        return flattened

    def possible_knight_moves(self):
        pass


class Pawn(Piece):

    def __init__(self, white, rank, file, board):
        super(Pawn, self).__init__(white=white, kind='pawn', x=rank, y=file, board=board)

    def possible_moves(self):
        """
        first pass - just in bounds forward pawn moves, account for first move.
        second pass - remove all moves where there's an occupied square ahead
        third pass - look for captures
        TODO Fourth pass -> en passant
        """
        moves = []
        if self.white:
            if self.has_moved:
                if self.rank < 7:
                    moves.append((self.rank - 1, self.file))
            else:
                moves.append((self.rank - 1, self.file))
                moves.append((self.rank - 2, self.file))
        else:
            if self.has_moved:
                if self.rank > 0:
                    moves.append((self.rank + 1, self.file))
            else:
                moves.append((self.rank + 1, self.file))
                moves.append((self.rank + 2, self.file))

        # can't move forward into another piece
        refined_moves = [(rank, file) for (rank, file) in moves if not self.board.is_occupied(rank, file)]

        # look for captures
        possible_captures = []
        if self.white:
            possible_captures.append((self.rank - 1, self.file - 1))
            possible_captures.append((self.rank - 1, self.file + 1))
        else:
            possible_captures.append((self.rank + 1, self.file - 1))
            possible_captures.append((self.rank + 1, self.file + 1))

        # only can capture if there's an enemy on that square
        refined_captures = [(rank, file) for (rank, file) in possible_captures if self.enemy_at(rank, file)]

        all_moves = refined_moves + refined_captures
        outer = list()
        outer.append(all_moves)
        return outer


class Rook(Piece):

    def __init__(self, white, rank, file, board):
        super(Rook, self).__init__(white=white, kind='rook', x=rank, y=file, board=board)

    def possible_moves(self):
        return [Positions.right_moves(self.rank, self.file),
                Positions.left_moves(self.rank, self.file),
                Positions.up_moves(self.rank, self.file),
                Positions.down_moves(self.rank, self.file)]


class Knight(Piece):

    def __init__(self, white, rank, file, board):
        super(Knight, self).__init__(white=white, kind='knight', x=rank, y=file, board=board)

    def possible_moves(self):
        move_combinations = [
            (self.rank + 1, self.file + 2),
            (self.rank + 1, self.file - 2),
            (self.rank + 2, self.file + 1),
            (self.rank + 2, self.file - 1),
            (self.rank - 1, self.file + 2),
            (self.rank - 1, self.file - 2),
            (self.rank - 2, self.file + 1),
            (self.rank - 2, self.file - 1)
        ]
        # now filter out those that went out of bounds
        in_range_moves = []
        for (rank, file) in move_combinations:  # singleton
            if 0 <= rank < 8 and 0 <= file < 8:
                in_range_moves.append((rank, file))
        return in_range_moves

    def legal_moves(self):
        """
        Legal moves are different for knights - they can hop over pieces.
        """
        return [(rank, file) for (rank, file) in self.possible_moves() if not self.friendly_at(rank, file)]


class Bishop(Piece):

    def __init__(self, white, rank, file, board):
        super(Bishop, self).__init__(white=white, kind='bishop', x=rank, y=file, board=board)

    def possible_moves(self):
        return [Positions.diag_up_right_moves(self.rank, self.file),
                Positions.diag_up_left_moves(self.rank, self.file),
                Positions.diag_down_right_moves(self.rank, self.file),
                Positions.diag_down_left_moves(self.rank, self.file)]


class Queen(Piece):

    def __init__(self, white, rank, file, board):
        super(Queen, self).__init__(white=white, kind='queen', x=rank, y=file, board=board)

    def possible_moves(self):
        return [
            Positions.diag_up_right_moves(self.rank, self.file),
            Positions.diag_up_left_moves(self.rank, self.file),
            Positions.diag_down_right_moves(self.rank, self.file),
            Positions.diag_down_left_moves(self.rank, self.file),
            Positions.right_moves(self.rank, self.file),
            Positions.left_moves(self.rank, self.file),
            Positions.up_moves(self.rank, self.file),
            Positions.down_moves(self.rank, self.file)
        ]


class King(Piece):
    def __init__(self, white, rank, file, board):
        super(King, self).__init__(white=white, kind='king', x=rank, y=file, board=board)

    def possible_moves(self):
        move_list = list()
        for x in range(self.rank - 1, self.rank + 2):
            for y in range(self.file - 1, self.file + 2):
                if 8 > x > 0 and 8 > y > 0:
                    if not (x == self.rank and y == self.file):
                        move_list.append(list((x, y)))
        return move_list
