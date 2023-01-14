import numpy as np


def cleared_rows(field):
    '''
        returns the number of rows that will be cleared in this field
        :param field:
        :return: total number of rows cleared
    '''
    cleared_r = 0

    for row in field:
        if all([x != 0 for x in row]):
            cleared_r += 1
    return cleared_r


def max_height(field):
    max_h = len(field)
    for row in field:
        if any([x != 0 for x in row]):
            return max_h
        else:
            max_h = max_h - 1
    return max_h


# source of the idea: https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/
def avg_height(field):
    max_heights = [len(field) for _ in range(len(field[0]))]
    ones = [False for _ in range(len(field[0]))]

    for row in field:
        for i, col in enumerate(row):
            if col != 0:
                ones[i] = True
            if not ones[i]:
                max_heights[i] = max_heights[i] - 1
    return np.mean(max_heights)


def number_of_holes(field):
    holes = 0
    ones = [False for _ in range(len(field[0]))]

    for row in field:
        for i, col in enumerate(row):
            if col != 0:
                ones[i] = True
            if col == 0 and ones[i]:
                holes += 1
    return holes


def bumpiness(field):
    bumps = 0
    zeros = [False for _ in range(len(field[0]))]

    for row in field[::-1]:
        for i, col in enumerate(row):
            if col == 0:
                zeros[i] = True
            if col != 0 and zeros[i]:
                bumps += 1
    return bumps

