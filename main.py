# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from model.Board import Board
from model import Conversions
from model.Piece import Piece, Pawn


def tests():
    board = Board(fen='r1b1k2r/ppppqNpp/2n2n2/4p3/2B1P3/8/PPPP1KPP/RNBQ3R w kq - 1 7')
    print(board)
    black_knight = board.piece_at('f6')
    print(moves_ext(black_knight.legal_moves()))

    #
    # board = Board()
    # pawn = Pawn(white=True, rank='5', file='6', board=board)
    # print(pawn)



def moves_ext(moves):
    return [Conversions.internal_to_algebraic(move) for move in moves]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tests()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
