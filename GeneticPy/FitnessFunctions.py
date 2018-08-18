import numpy as np


class _FitnessFunctionBase:
    def __init__(self, data=None):
        pass

    def evaluate(self):
        raise NotImplementedError


class KQueens(_FitnessFunctionBase):
    def __init__(self, data):
        null_list = np.full(data, -1)
        self.numbers_window = np.concatenate((null_list, np.arange(0, data), null_list))
        self.inverse_window = np.concatenate((null_list, np.arange(data - 1, -1, -1), null_list))

    def evaluate(self, individual):
        genotype = individual.genotype

        n = len(genotype)

        fitness = 0
        for i in range(0, n * 2 - 1):
            coalitions = 0
            inv_coalitions = 0

            for j in range(0, n):
                if genotype[j] == self.numbers_window[j + i]:
                    coalitions += 1
                if genotype[j] == self.inverse_window[j + i]:
                    inv_coalitions += 1

            if coalitions > 1:
                fitness += coalitions
            if inv_coalitions > 1:
                fitness += inv_coalitions
        return fitness


class QAP(_FitnessFunctionBase):
    def __init__(self, data):
        self.A = data['A']
        self.B = data['B']
        self.n = data['n']

    def evaluate(self, individual):
        genotype = individual.genotype
        value = 0
        """
        Objective function is defined as:
        Sum(W(i,j)*D(f(i),f(j)) for all i,j from {1, 2, ..., n}

        Where f(n) is our proposed mapping from "n" factories/symbols
        to "n" locations, W is the flow matrix, and D is the distance
        matrix
        """

        for i in range(self.n):
            for j in range(i + 1, self.n):
                """
                Function f(n) = genotype[n] - 1, represents the
                assignment of Symbol/Factory "n" to location j.
                in other words, f(n) its our proposed
                solution off assignment of "n" symbols to "n"
                locations

                r = f(i) = genotype[i] - 1
                Here we calculate assignment of Symbol "i" to
                location f(i) and storing it on r, this process
                repeats for "j" and is stored on c
                """
                r = genotype[i] - 1
                c = genotype[j] - 1

                # print("i = {}, j = {}, r = {}, c = {}".format(i, j, r, c))

                """
                Recall A is or Weight matrix, and B our distance matrix.
                We consider two cases with indexes i,j and j,i. In case
                matrix A or B aren't symmetrical
                W(i,j) * D(f(i),f(j)) + W(j,i) * D(f(j),f(i))
                """
                value += self.A[i][j] * self.B[r][c] + self.A[j][i] * self.B[c][r]
        return value
