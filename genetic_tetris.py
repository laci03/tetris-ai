import copy
import heuristics

# Shapes of the blocks
shapes = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],
    [[4, 5, 9, 10], [2, 6, 5, 9]],
    [[6, 7, 9, 10], [1, 5, 6, 10]],
    [[2, 1, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
    [[1, 2, 6, 10], [5, 6, 7, 9], [1, 5, 9, 10], [3, 5, 6, 7]],
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    [[1, 2, 5, 6]],
]


class GeneticTetris:
    def __init__(self, tetris, heuristics_weight):
        self.tetris = copy.deepcopy(tetris)

        self.heuristics_weight = heuristics_weight
        self.all_fields = self.generate_all_moves()

    def generate_all_moves(self):
        all_fields = []
        # print('block type: {}, next_block type: {}'.format(self.tetris.block.type, self.tetris.nextBlock.type))

        possibilities = 0
        initial_field = copy.deepcopy(self.tetris.field)
        initial_tetris_type = self.tetris.block.type

        for rotation in range(len(shapes[self.tetris.block.type])):
            self.tetris.block.rotation = rotation
            self.tetris.block.type = initial_tetris_type

            tetris_x_min, tetris_x_max = self.get_tetris_min_max(self.tetris.block)

            for tetris_x in range(tetris_x_min, tetris_x_max + 1, 1):
                self.tetris.field = copy.deepcopy(initial_field)

                self.tetris.block.x = tetris_x
                self.tetris.block.y = 0
                self.tetris.block.rotation = rotation
                self.tetris.block.type = initial_tetris_type

                # print('rotation {}, tetris_x {}'.format(rotation, tetris_x))

                self.generate_field()
                next_field = copy.deepcopy(self.tetris.field)

                for next_rotation in range(len(shapes[self.tetris.nextBlock.type])):
                    self.tetris.nextBlock.rotation = next_rotation
                    next_tetris_x_min, next_tetris_x_max = self.get_tetris_min_max(self.tetris.nextBlock)

                    for next_tetris_x in range(next_tetris_x_min, next_tetris_x_max + 1, 1):
                        self.tetris.field = copy.deepcopy(next_field)
                        possibilities += 1

                        self.tetris.block.x = next_tetris_x
                        self.tetris.block.y = 0
                        self.tetris.block.type = self.tetris.nextBlock.type
                        self.tetris.block.rotation = next_rotation

                        self.generate_field()

                        current_field = self.tetris.field

                        current_fitness = heuristics.max_height(current_field) * self.heuristics_weight[0] + \
                                          heuristics.cleared_rows(current_field) * self.heuristics_weight[1] + \
                                          heuristics.avg_height(current_field) * self.heuristics_weight[2] + \
                                          heuristics.number_of_holes(current_field) * self.heuristics_weight[3] + \
                                          heuristics.bumpiness(current_field) * self.heuristics_weight[4]

                        all_fields.append(((tetris_x, rotation), copy.deepcopy(self.tetris.field), current_fitness))

        # print('total number of maps: {}'.format(possibilities))

        return all_fields

    def generate_field(self):
        while not self.tetris.intersects():
            self.tetris.block.y += 1
        self.tetris.block.y -= 1

        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetris.block.image():
                    self.tetris.field[i + self.tetris.block.y][j + self.tetris.block.x] = self.tetris.block.color

    @staticmethod
    def pprint_map(field):  # for debugging purposes only
        for f in field:
            print(f)

    @staticmethod
    def get_tetris_min_max(block):
        tetris_x_min = 0
        if all([x % 4 != 0 for x in shapes[block.type][block.rotation]]):
            tetris_x_min = - 1

        aux = -1
        for x in shapes[block.type][block.rotation]:
            if x % 4 > aux:
                aux = x % 4

        tetris_x_max = 9 - aux

        # print(tetris_x_min, tetris_x_max)
        return tetris_x_min, tetris_x_max

    def next_move(self):
        return sorted(self.all_fields, key=lambda x: x[-1], reverse=True)[0][0]


if __name__ == '__main__':
    from tetris import *

    game = Tetris(20, 10)

    game.new_block()
    game.next_block()
    heuristics_weight = [-3, 5.9, -3, -3, -2.8]

    ai_agent = GeneticTetris(game, heuristics_weight)

    print(ai_agent.next_move())
