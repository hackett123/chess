"""
Board and Piece both have to go between algebraic and our 2d representation at times, so share functionality here
"""


# example: [6, 4] is e2, [6, 3] is d2
def internal_to_algebraic(position):
    rank, file = position
    letter = chr(int(ord('a')) + file)
    number = 8 - rank

    return letter + str(number)


def algebraic_to_internal(square):
    rank_number = square[1]  # 1, 2, ... 8 -> off by one and upside down
    file_letter = square[0]  # a, b, ..., h

    rank = 8 - int(rank_number)
    file = ord(file_letter) - int(ord('a'))

    return rank, file
