
## Fitness function implementation
# F : R - > R
# We have a solution X (x1,x2,x3)

# Decision variables x1, x2 ...
# and their objective values : y1, y2 ...

# calculate Fitness values
# We need this value in the mating selection process


class Fitness_impl:

    # we are maximizing, so we want to get the fitness values to be maximal

    move_threshold = 100
    multiplier_won = 10
    multiplier_lost = 0.1

    def calculate_fitness (self,objective_values):
        if len(objective_values) == 0:
            return 0
        score_achieved = objective_values[0]
        number_of_moves = objective_values[1]

        # longer games are better rewarded
        if self.move_threshold <= number_of_moves:
            fitness_multiplier = self.multiplier_won
        else:
            fitness_multiplier = self.multiplier_lost

        fitness = score_achieved / number_of_moves
        fitness = fitness * fitness_multiplier

        return fitness

