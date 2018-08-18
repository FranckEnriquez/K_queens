
from Crossovers import cut_and_cross_fill, order_crossover
from Mutation import swap, inversion
from FitnessFunctions import KQueens, QAP
from GeneticAlgorithm import GeneticAlgorithm, _Individual
from GeneticAlgoritmUtils import print_board, read_qap_entry_from_file
import numpy as np
import random


def debug_tests():
    parent_1 = _Individual(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    parent_2 = _Individual(np.array([9, 3, 7, 8, 2, 6, 5, 1, 4]))
    #order_crossover(parent_1, parent_2, random)
    inversion(parent_1, random)

def k_queens_config():
    max_generations = 20000
    queens = 64
    parameters = {'population_size': 100,
                  'fitness_function': KQueens(queens),
                  'variable_qty': queens,
                  'lower_bound': 0,
                  'max_generations': max_generations,
                  'crossover_operator': order_crossover, 'crossover_probability': 0.9,
                  'mutation_operator': swap, 'mutation_probability': 0.6}

    ga = GeneticAlgorithm(parameters)
    solution = ga.evolve(True)
    print_board(solution)
    ga.print_fitness_curve()


def qap_config():
    file_names = ["lipa20a", "tai35a", "kra30a", "tho40"]
    sub_optimals = [1, 3]
    test_objective_function = False
    i = 2

    qap_input = read_qap_entry_from_file("QAP_instances/{}".format(file_names[i]))
    optimal_value = qap_input["optimal_value"]
    n = qap_input["n"]

    max_generations = 10000
    parameters = {'population_size': 100,
                  'fitness_function': QAP(qap_input),
                  'variable_qty': n,
                  'max_generations': max_generations,
                  'crossover_operator': cut_and_cross_fill, 'crossover_probability': 1,
                  'mutation_operator': swap, 'mutation_probability': 1}

    legend = "known at the moment: "
    if "optimal_solution" in qap_input:
        legend = "is optimal: "
        parameters['lower_bound'] = optimal_value
    ga = GeneticAlgorithm(parameters)
    solution = ga.evolve(True)

    print("The best solution {} {} while yours is {}".format(legend, optimal_value, solution.fitness))
    print("The best found solutions fails by: {}%".format((round(solution.fitness / optimal_value - 1, 4))*100))

    ga.print_fitness_curve()

#qap_config()
#debug_tests()
k_queens_config()