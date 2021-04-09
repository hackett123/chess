"""
up is down and down is up. a little ender's gamey in that direction doesn't matter since
it all comes in pairs.
"""


def right_moves(rank, file):
    return [(right, file) for right in range(rank + 1, 8)]


def left_moves(rank, file):
    return [(left, file) for left in range(0, rank)]


def up_moves(rank, file):
    return [(rank, up) for up in range(rank + 1, 8)]


def down_moves(rank, file):
    return [(rank, down) for down in range(0, rank)]


def diag_up_right_moves(rank, file):
    dist_to_edge = min(8 - rank, 8 - file)
    return [(rank + i, file + i) for i in range(1, dist_to_edge)]


def diag_up_left_moves(rank, file):
    dist_to_edge = min(rank, 8 - file)
    return [(rank - i, file + i) for i in range(1, dist_to_edge)]


def diag_down_right_moves(rank, file):
    dist_to_edge = min(8 - rank, file)
    return [(rank + i, file - i) for i in range(1, dist_to_edge)]


def diag_down_left_moves(rank, file):
    dist_to_edge = min(rank, file)
    return [(rank - i, file - i) for i in range(1, dist_to_edge)]
