import numpy as np
from GeneticAlgorithm import  _Individual


def swap(offspring, random_generator):
    genotype = offspring.genotype

    n = len(genotype)

    mutated_offspring = np.copy(genotype)

    x = random_generator.randint(0, n - 1)
    y = random_generator.randint(0, n - 1)

    val1 = mutated_offspring[x]
    val2 = mutated_offspring[y]

    mutated_offspring[y] = val1
    mutated_offspring[x] = val2

    return _Individual(mutated_offspring)


def inversion(offspring, random_generator):
    n = len(offspring.genotype)
    i, j = sorted([random_generator.randint(0, n), random_generator.randint(0, n)])

    mutated_genotype = np.copy(offspring.genotype)
    mutated_genotype[i:j] = np.flip(offspring.genotype[i:j], axis=0)

    return _Individual(mutated_genotype)
