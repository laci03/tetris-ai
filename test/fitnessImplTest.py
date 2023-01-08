import unittest
import fitness_impl

# these tests are not good
# marking them skipped would be a great option

class MyTestCase(unittest.TestCase):
    def test_game_won(self):
        under_test = fitness_impl.Fitness_impl
        score = 10000
        move_count = 100
        values = [score, move_count]
        fitness = under_test.calculate_fitness(fitness_impl.Fitness_impl,values)
        self.assertEqual(fitness, 1000)

    def test_game_over(self):
        under_test = fitness_impl.Fitness_impl
        score = 100
        move_count = 10
        values = [score, move_count]
        fitness = under_test.calculate_fitness(under_test,values)
        self.assertEqual(fitness, 1)

    def test_empty_game(self):
        under_test = fitness_impl.Fitness_impl
        values = []
        fitness = under_test.calculate_fitness(under_test,values)
        self.assertEqual(fitness, 0)


if __name__ == '__main__':
    unittest.main()
