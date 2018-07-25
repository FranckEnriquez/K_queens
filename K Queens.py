import random
import matplotlib.pyplot as plt




class individual():
    def __init__(self, queens, fitness=0):
        self.queens = queens
        self.fitness = fitness

class kQueens():
    def __init__(self, queenquantity, populationSize):
        self.queenQuantity = queenquantity
        self.population = list()

        self.numbersWindow = list()
        self.inverseNumbers = list()
        self.populationSize = populationSize
        
        self.x_generation = list()
        self.y_fitness = list()
    
    def print_fitness_curve(self):
        plt.step(self.x_generation, self.y_fitness, histtype='step')
        plt.show()

    def evolve(self):

        generations = 1
        self.initializePopulation()

        maxIndiv = max(self.population, key = lambda x: x.fitness)
        
        self.x_generation.append(0)
        self.y_fitness.append(maxIndiv.fitness)
        
        lastFitness = 0

        while generations <= 20000:


            matingParents = self.selectParents()

            self.cross(matingParents[0].queens, matingParents[1].queens)

            self.selectSurvival()

            maxIndiv = self.population[self.populationSize - 1]

            if lastFitness != maxIndiv.fitness:
                self.x_generation.append(generations)
                self.y_fitness.append(maxIndiv.fitness)
            lastFitness = maxIndiv.fitness


            if maxIndiv.fitness == 0:
                break;

            generations += 1
            text = "Generation: " + str(generations) + " Max Fitness: " + str(maxIndiv.fitness)
            print(text)
        print(maxIndiv.queens)

        self.printBoard(maxIndiv.queens)

        return generations

    def initializePopulation(self):
        # Initialize comparision arrays
        nullList = list()
        for i in range(self.queenQuantity):
            nullList.append(-1)
            self.numbersWindow.append(-1)
            self.inverseNumbers.append(-1)

        self.numbersWindow.extend(list(range(0, self.queenQuantity)))
        self.inverseNumbers.extend(list(range(self.queenQuantity - 1, -1, -1)))

        self.numbersWindow.extend(nullList)
        self.inverseNumbers.extend(nullList)

        # Initialize population
        numbers = list(range(self.queenQuantity))
        for i in range(self.populationSize):
            random.shuffle(numbers)
            indiv = individual(numbers.copy(), self.fitnessFunction(numbers))

            self.population.append(indiv)

    def cross(self, father, mother):
        crossPoint = random.randrange(0, self.queenQuantity, 1)

        child = list()
        childTwo = list()

        # Initialice offspring
        for i in range(0, self.queenQuantity):
            child.append(-1)
            childTwo.append(-1)

        # Copy part o the genetic material from the parents
        for i in range(0, crossPoint + 1):
            child[i] = father[i]
            childTwo[i] = mother[i]

        '''
            Cross genotypes of both parents

            offset1 y offset2 are flags used to 
            indicate the last modified index
        '''
        offset1 = crossPoint + 1
        offset2 = crossPoint + 1
        for i in range(crossPoint + 1, self.queenQuantity):
            if mother[i] not in child:
                child[offset1] = mother[i]
                offset1 += 1
            if father[i] not in childTwo:
                childTwo[offset2] = father[i]
                offset2 += 1

        # Complete missing genes
        for i in range(0, crossPoint + 1):
            if mother[i] not in child:
                child[offset1] = mother[i]
                offset1 += 1
            if father[i] not in childTwo:
                childTwo[offset2] = father[i]
                offset2 += 1

        indiv = individual(child)
        indivTwo = individual(childTwo)

        self.mutation(child)
        self.mutation(childTwo)


        indiv.fitness = self.fitnessFunction(child)

        indivTwo.fitness = self.fitnessFunction(childTwo)

        self.population.append(indiv)
        self.population.append(indivTwo)

    def mutation(self, genotype):
        randomNumber = random.randrange(0, 101, 1)
        if randomNumber <= 80:
            x = random.randrange(0, self.queenQuantity, 1)
            y = random.randrange(0, self.queenQuantity, 1)

            val1 = genotype[x]
            val2 = genotype[y]

            genotype[y] = val1
            genotype[x] = val2

        return genotype

    def selectSurvival(self):
        self.population = sorted(self.population, key=lambda x: x.fitness)
        self.population = self.population[2:]

    def selectParents(self):
        selectedParents = list()
        for i in range(0, 5):
            randonNumber = random.randrange(0, self.populationSize)
            selectedParents.append(self.population[randonNumber])

        selectedParents = sorted(selectedParents, key=lambda x: x.fitness, reverse=True)

        return selectedParents[0:2]

    def fitnessFunction(self, genotype):
        collitions = 0
        invCollitions = 0
        fitness = 0
        for i in range(0, self.queenQuantity * 2 - 1):
            collitions = 0
            invCollitions = 0

            for j in range(0, self.queenQuantity):
                if genotype[j] == self.numbersWindow[j + i]:
                    collitions += 1
                if genotype[j] == self.inverseNumbers[j + i]:
                    invCollitions += 1

            if collitions > 1:
                fitness += collitions
            if invCollitions > 1:
                fitness += invCollitions
        return fitness * -1
    
    
    def printBoard(self, queens):
        for i in range(0, self.queenQuantity):
            text = ""
            for j in range(0, self.queenQuantity):
                if queens[j] == i:
                    text += "[Q]"
                else:
                    text += "[ ]"
            print(text)




k = 64

queens = kQueens(k, 100)
res = queens.evolve()

x = queens.x_generation
y = queens.y_fitness
plt.step(x, y, where = 'post')
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.show()



#colony = ACO(8, 50)
#colony.explore(5000)


