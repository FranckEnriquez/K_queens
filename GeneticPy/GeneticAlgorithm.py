import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


class GeneticAlgorithm:
    def __init__(self, parameters):
        self.population_size = parameters['population_size']
        self.fitness_function = parameters['fitness_function']
        self.cross_parents = parameters['crossover_operator']
        self.crossover_probability = parameters['crossover_probability']
        self.mutation_operator = parameters['mutation_operator']
        self.mutation_probability = parameters['mutation_probability']
        self.max_generations = parameters['max_generations']
        self.variable_qty = parameters['variable_qty']
        self.lower_bound = parameters['lower_bound']

        # Internal fields
        self._population = None
        self.run_information = np.empty((0, 2))
        self._best_individual = None
        self._generation = None

    def evolve(self, print_generations=False):
        self._initialize_population()

        # Sets generation to zero, to start evolving
        self._generation = 0

        # Sets min fitness to maximum possible value
        min_fitness = float('inf')

        # Evolve population
        while not self._termination_condition():
            # Select parents
            parent_1, parent_2 = self._select_parents()


            # Cross
            if random.uniform(0, 1) <= self.crossover_probability:
                # Will cross
                offspring_1, offspring_2 = self.cross_parents(parent_1, parent_2, random)
            else:
                # Will not cross
                offspring_1, offspring_2 = parent_1, parent_2

            # Mutate
            if random.uniform(0, 1) <= self.mutation_probability:
                offspring_1 = self.mutation_operator(offspring_1, random)
            if random.uniform(0, 1) <= self.mutation_probability:
                offspring_2 = self.mutation_operator(offspring_2, random)

            # Evaluate fitness of offspring
            offspring_1.fitness = self.fitness_function.evaluate(offspring_1)
            offspring_2.fitness = self.fitness_function.evaluate(offspring_2)

            # Add offspring to population
            self._population.extend((offspring_1, offspring_2))

            # Survival selection
            self._select_survivors()

            self._generation += 1

            # Saves best individual
            self._best_individual = self._population[0]

            # Fitness curve update if best fitness improved
            # Updates fitness curve data
            if self._best_individual.fitness < min_fitness:
                min_fitness = self._best_individual.fitness
                self.run_information = np.vstack((self.run_information,[self._generation, self._best_individual.fitness]))

            # Prints information
            if print_generations:
                print("Generation: " + str(self._generation) + " min_fitness: " + str(self._best_individual.fitness))
        return self._best_individual

    def _initialize_population(self):
        self._population = list()

        for i in range(self.population_size):
            genotype = list(range(0, self.variable_qty))
            random.shuffle(genotype)
            individual = _Individual(np.array(genotype))
            individual.fitness = self.fitness_function.evaluate(individual)
            self._population.append(individual)

    def _select_parents(self):
        selected_parents = list()
        for i in range(0, 5):
            random_number = random.randint(0, self.population_size - 1)
            selected_parents.append(self._population[random_number])

            selected_parents = sorted(selected_parents, key=lambda x: x.fitness)

        return selected_parents[0], selected_parents[1]

    def _select_survivors(self):
        self._population = sorted(self._population, key=lambda x: x.fitness)
        self._population = self._population[:100]

    def _termination_condition(self):
        if self._generation >= self.max_generations:
            return True
        elif self.lower_bound is not None:
            return False if self._best_individual is None else self._best_individual.fitness <= self.lower_bound

    def print_fitness_curve(self):
        x = self.run_information[:, 0]
        y = self.run_information[:, 1]
        plt.step(x, y, where='post')
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.show()


class _Individual:
    def __init__(self, genome=None, fitness=None, individual=None):
        self.genotype = genome
        self.fitness = fitness

        if individual is not None:
            self.genotype = individual.genome
            self.fitness = individual.fitness
