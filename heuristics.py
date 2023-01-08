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
def aggregate_height(field):
    return 0


def avg_height(field):
    return 0


def number_of_holes(field):
    return 0


def bumpiness(field):
    return 0

