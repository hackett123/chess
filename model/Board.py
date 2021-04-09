from model import FEN, Conversions
from model.Piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:

    def __init__(self, fen=None):
        self.start_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        if not fen:
            fen = self.start_fen

        self.board_as_string = FEN.read_fen(fen)
        self.board = self.init_pieces()
        self.white_castles_king, self.white_castles_queen, self.black_castles_king, self.black_castles_queen = FEN.castle_info(
            fen)
        self.white_to_move = FEN.who_moves(fen)
        self.fifty_move_count = FEN.plies_since_capture(fen)
        self.move_number = FEN.move_number(fen)
        self.ply_number = self.move_number * 2

    def copy_board(self):
        new_board = []
        for rank in self.board:
            new_rank = []
            for piece in rank:
                if piece:
                    new_rank.append(piece.copy())
                else:
                    new_rank.append(None)
            new_board.append(new_rank)
        return new_board

    def board_to_string(self):
        str_rep = ''
        for rank_contents in self.board:
            for piece in rank_contents:
                if piece:
                    str_rep += str(piece) + ' '
                else:
                    str_rep += '_ '
            str_rep += '\n'
        return str_rep
        # return '\n'.join([' '.join(rank) for rank in self.board])

    def init_pieces(self):

        fen_to_pieces = {
            'p': 'pawn',
            'r': 'rook',
            'n': 'knight',
            'b': 'bishop',
            'q': 'queen',
            'k': 'king'
        }

        board = []

        for rank_index in range(len(self.board_as_string)):
            rank_contents = self.board_as_string[rank_index]
            rank = []
            for file_index in range(len(rank_contents)):
                piece = rank_contents[file_index]
                if not piece == ' ':
                    white = str.isupper(piece)
                    kind = fen_to_pieces[str.lower(piece)]
                    if kind == 'pawn':
                        rank.append(Pawn(white, rank_index, file_index, self))
                    elif kind == 'rook':
                        rank.append(Rook(white, rank_index, file_index, self))
                    elif kind == 'knight':
                        rank.append(Knight(white, rank_index, file_index, self))
                    elif kind == 'bishop':
                        rank.append(Bishop(white, rank_index, file_index, self))
                    elif kind == 'queen':
                        rank.append(Queen(white, rank_index, file_index, self))
                    elif kind == 'king':
                        rank.append(King(white, rank_index, file_index, self))
                else:
                    rank.append(None)
            board.append(rank)
        return board

    def is_occupied(self, rank, file):
        return self.board[rank][file]

    # using our internal representation of 2d list
    def piece_at_internal(self, rank, file):
        return self.board[rank][file]

    # uses algebraic notation
    def piece_at(self, square):
        (rank, file) = Conversions.algebraic_to_internal(square)
        return self.piece_at_internal(rank, file)

    # note that this isn't truly external notation, as right now we expect the full algebraic notation of from,
    # to. does not account for capturing notation nor how pawn moves are written (as well as some rook moves,
    # knight moves...) Returns Boolean - true if moved However, note that the "external" notation is for recording
    # moves - our input comes from the move itself, and recording that move for our records is not part of this
    # functionality
    def move_piece_external(self, old_square, new_square):
        (from_rank, from_file) = Conversions.algebraic_to_internal(old_square)
        (to_rank, to_file) = Conversions.algebraic_to_internal(new_square)
        print('moving from', from_rank, from_file)
        print('moving to', to_rank, to_file)
        if self.move_piece_internal(from_rank, from_file, to_rank, to_file):
            self.ply_number += 1
            if not (self.ply_number % 2): self.move_number += 1

    def move_piece_internal(self, from_rank, from_file, to_rank, to_file):
        # verify piece exists there
        piece = self.piece_at_internal(from_rank, from_file)
        if piece:
            # verify move to destination is legal
            if (to_rank, to_file) in piece.legal_moves():
                destination_piece = self.piece_at_internal(to_rank, to_file)
                if destination_piece:
                    # remove piece at from location if exists
                    self.remove_piece(to_rank, to_file)
                self.update_piece(piece, to_rank, to_file)
                return True
            else:
                print('move is not legal!')
                return False

    def remove_piece(self, rank, file):
        self.board[rank][file] = None

    def update_piece(self, piece, to_rank, to_file):
        # we don't delete the old piece and make a new one here bc we want to remember that it has moved
        self.board[piece.rank][piece.file] = None
        self.board[to_rank][to_file] = piece
        piece.rank, piece.file = to_rank, to_file

    def __str__(self):
        info = list()

        # board
        info.append(self.board_to_string())

        # # castling
        # if self.white_castles_king and self.white_castles_queen:
        #     info.append('White can castle both king and queen side.')
        # elif self.white_castles_king:
        #     info.append('White can castle king side.')
        # elif self.white_castles_queen:
        #     info.append('White can castle queen side.')
        # else:
        #     info.append('White cannot castle.')
        #
        # if self.black_castles_king and self.black_castles_queen:
        #     info.append('Black can castle both king and queen side.')
        # elif self.black_castles_king:
        #     info.append('Black can castle king side.')
        # elif self.black_castles_queen:
        #     info.append('Black can castle queen side.')
        # else:
        #     info.append('Black cannot castle.')

        # moves, who's up
        info.append('White to move' if self.white_to_move else 'Black to move')
        info.append(f'Move Number: {self.move_number}')
        info.append(f'{self.fifty_move_count} plies since last capture or pawn advance.')

        return '\n'.join(info)
