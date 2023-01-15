import argparse
import os
import random

import pandas as pd

from tetris import Tetris
from tqdm import tqdm


def init_chromosome(ch_length):
    return [random.uniform(-1, 1.1),  # max_height weight
            random.uniform(-1, 1.1),  # cleared_rows weight
            random.uniform(-1, 1.1),  # avg_height weight
            random.uniform(-1, 1.1),  # number_of_holes weight
            random.uniform(-1, 1.1)  # bumpiness weight
            ]


def mutate_chromosome(chromosome, mutation_prob):
    # reset mutation with a probability of mutation_prob
    return [x if random.uniform(0, 1) > mutation_prob else random.uniform(-1, 1.1) for x in chromosome]


def crossover(chromosome_1, chromosome_2):
    if random.uniform(0, 1) < 0.05:  # 5 percentage probability to copy the parents as they are in the new generation
        return chromosome_1, chromosome_2
    else:   # n point crossover
        crossover_perc = [random.uniform(0, 1) for _ in chromosome_1]

        new_chromosome_1 = [x if cr_p < 0.5 else (x + y) / 2 for x, y, cr_p in
                            zip(chromosome_1, chromosome_2, crossover_perc)]
        new_chromosome_2 = [y if cr_p >= 0.5 else (x + y) / 2 for x, y, cr_p in
                            zip(chromosome_1, chromosome_2, crossover_perc)]

        return new_chromosome_1, new_chromosome_2


def main(number_of_moves, number_of_generations, population_size, ch_length, mutation_prob, elitism_perc,
         output_folder):
    # create output folder
    os.makedirs(output_folder, exist_ok=True)

    # init chromosomes
    chromosomes = [init_chromosome(ch_length) for _ in range(population_size)]

    for generation in range(number_of_generations):
        random_seed = random.randint(0, 1000000)
        scores = []
        moves_array = []

        for chromosome in tqdm(chromosomes, desc='Generation: {}'.format(generation)):
            random.seed(random_seed)  # select a random seed so each chromosome will play the same game
            tetris_game = Tetris(20, 10, chromosome)
            moves = 0

            tetris_game.new_block()
            tetris_game.next_block()

            while tetris_game.state == 'start' and moves <= number_of_moves:
                tetris_game.moveBottom()
                moves += 1

            scores.append(tetris_game.score)
            moves_array.append(moves)

        # sort the chromosomes based on their achieved score
        chromosomes_scores = list(zip(scores, chromosomes, moves_array))
        chromosomes_scores = sorted(chromosomes_scores, key=lambda x: x[0], reverse=True)

        # save the generation with their achieved score and each genome move
        df = pd.DataFrame([x[1] for x in chromosomes_scores],
                          columns=['max_height', 'cleared_rows', 'avg_height', 'number_of_holes', 'bumpiness'])
        df['score'] = [x[0] for x in chromosomes_scores]
        df['moves'] = [x[2] for x in chromosomes_scores]

        df.to_csv(os.path.join(output_folder, 'generation_{}_seed_{}.csv'.format(generation, random_seed)))

        # create the new generation
        # the first elitism_perc will go automatically in the new generation
        new_chromosomes = [chromosome[1] for chromosome in
                           chromosomes_scores[:int(len(chromosomes_scores) * elitism_perc)]]

        # for the rest, we randomly select 2 paraets and do cross over
        new_population_size = len(new_chromosomes)
        while new_population_size < population_size:
            ch_1, ch_2 = random.sample(chromosomes, 2)

            new_chromosomes.extend(crossover(ch_1, ch_2))

            new_population_size += 2

        # for each chromosome we add also mutation
        chromosomes = [mutate_chromosome(new_chromosome, mutation_prob) for new_chromosome in
                       new_chromosomes[:population_size]]


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--number_of_generations', type=int, default=100,
                        help='the number of generations that the algorithm should be trained')
    parser.add_argument('--population_size', type=int, default=40,
                        help='the size of the population that each generation should contain')
    parser.add_argument('--ch_length', type=int, default=5,
                        help='the length of the chromosome')
    parser.add_argument('--mutation_prob', type=float, default=0.05,
                        help='the probability of a mutation')

    parser.add_argument('--number_of_moves', type=int, default=500,
                        help='the length of the game')

    parser.add_argument('--elitism_perc', type=float, default=0.2,
                        help='the percentage of top chromosomes that we move into the next generation')

    parser.add_argument('--output_folder', type=str, default='./models',
                        help='the folder where the models should be saved')

    return vars(parser.parse_args())


if __name__ == '__main__':
    args = get_args()

    main(args['number_of_moves'], args['number_of_generations'], args['population_size'],
         args['ch_length'], args['mutation_prob'], args['elitism_perc'], args['output_folder'])
