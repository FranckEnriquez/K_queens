import numpy as np

from GeneticAlgorithm import _Individual


def cut_and_cross_fill(parent_1, parent_2, random_generator):
    genotype_1, genotype_2 = parent_1.genotype, parent_2.genotype

    n = len(genotype_1)
    cross_point = random_generator.randint(0, n - 1)

    offspring_genotype_1, offspring_genotype_2 = np.full(n, -1), np.full(n, -1)

    # Copy part o the genetic material from the parents
    offspring_genotype_1[0:cross_point] = genotype_1[0:cross_point]
    offspring_genotype_2[0:cross_point] = genotype_1[0:cross_point]

    '''
        Cross genotypes of both parents

        offset1 y offset2 are flags used to 
        indicate the last modified index
    '''
    offset1 = cross_point
    offset2 = cross_point
    for i in range(cross_point, n):
        if genotype_2[i] not in offspring_genotype_1:
            offspring_genotype_1[offset1] = genotype_2[i]
            offset1 += 1
        if genotype_1[i] not in offspring_genotype_2:
            offspring_genotype_2[offset2] = genotype_1[i]
            offset2 += 1

    # Complete missing genes
    for i in range(0, cross_point):
        if genotype_2[i] not in offspring_genotype_1:
            offspring_genotype_1[offset1] = genotype_2[i]
            offset1 += 1
        if genotype_1[i] not in offspring_genotype_2:
            offspring_genotype_2[offset2] = genotype_1[i]
            offset2 += 1

    return _Individual(offspring_genotype_1), _Individual(offspring_genotype_2)


def order_crossover(parent_1, parent_2, random_generator):
    n = len(parent_1.genotype)
    i, j = sorted([random_generator.randint(0, n), random_generator.randint(0, n)])

    if i == j:
        return _Individual(parent_1.genotype), _Individual(parent_2.genotype)

    offspring_1_genotype = np.full(n, -1)
    offspring_2_genotype = np.full(n, -1)

    offspring_1_genotype[i:j] = parent_1.genotype[i:j]
    offspring_2_genotype[i:j] = parent_2.genotype[i:j]

    index_1, index_2 = 0 if j == n else j, 0 if j == n else j
    while -1 in offspring_1_genotype:
        if parent_2.genotype[index_2] not in offspring_1_genotype:
            offspring_1_genotype[index_1] = parent_2.genotype[index_2]
            index_1 = (index_1 + 1) if index_1 < n - 1 else 0

        index_2 = (index_2 + 1) if index_2 < n -1 else 0

    index_1, index_2 = 0 if j == n else j, 0 if j == n else j
    while -1 in offspring_2_genotype:
        if parent_1.genotype[index_1] not in offspring_2_genotype:
            offspring_2_genotype[index_2] = parent_1.genotype[index_1]
            index_2 = (index_2 + 1) if index_2 < n - 1 else 0
        index_1 = (index_1 + 1) if index_1 < n - 1 else 0

    return _Individual(offspring_1_genotype), _Individual(offspring_2_genotype)