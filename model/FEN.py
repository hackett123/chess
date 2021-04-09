"""
https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
Fen notation: slashes (/) divide rank information. Within each rank, a lowercase letter
denotes black pieces and uppercase denotes white. A number represents a sequence of empty
squares in the board.
The last segment contains the final rank and extra metadata:
    - whose turn it is (w or b)
    - castling information - a dash (-) if nobody can castle, K and/or Q for white can castle
        king or queen side, and a k and/or q for black can castle king or queen side
    - en passant target square - a dash(-) if none available currently
    - halfmoves since last capture
    - # of full moves, which increases after black moves
"""


def read_fen(fen):
    board = []
    rank_infos = fen.split('/')
    last_rank = rank_infos[-1].split(' ')[0]
    for rank_info in rank_infos:
        if rank_info == rank_infos[-1]:
            rank_info = last_rank
        rank = []
        for c in rank_info:
            if str.isnumeric(c):
                for i in range(int(c)):
                    rank.append(' ')
            else:
                rank.append(c)
        board.append(rank)
    return board


def castle_info(fen):
    """
    From a FEN, return a tuple of four boolean values denoting if white can castle king/queen side,
    black can castle king/queen side.
    """
    board_metadata = read_board_metadata(fen)
    availablity = board_metadata[1]
    return 'K' in availablity, 'Q' in availablity, 'k' in availablity, 'q' in availablity


def who_moves(fen):
    board_metadata = read_board_metadata(fen)
    return board_metadata[0] == 'w'


def plies_since_capture(fen):
    board_metadata = read_board_metadata(fen)
    return int(board_metadata[3])


def move_number(fen):
    board_metadata = read_board_metadata(fen)
    return int(board_metadata[4])


def read_board_metadata(fen):
    return fen.split('/')[-1].split(' ')[1:]
