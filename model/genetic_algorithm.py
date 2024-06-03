from random import randint


class GA:
    def __init__(self, param=None, problem_parameters=None):
        self.__param = param
        self.__problem_parameters = problem_parameters
        self.__population = []

    @property
    def population(self):
        return self.__population

    @property
    def param(self):
        return self.__param

    def one_generation_elitism(self):
        new_pop = [self.best_chromosome()]
        for _ in range(self.__param['popSize'] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            while self.__problem_parameters["generated"] is not None and off.representation in \
                    self.__problem_parameters["generated"]:
                off = p1.crossover(p2)
                off.mutation()
            if off.fitness > p1.fitness and off.fitness > p2.fitness:
                new_pop.append(off)
            elif p1.fitness > p2.fitness:
                new_pop.append(p1)
            else:
                new_pop.append(p2)
        self.__population = new_pop
        self.evaluation()

    def initialisation(self):
        for _ in range(0, self.__param['popSize']):
            c = self.__param["chromosome"](self.__problem_parameters)
            self.__population.append(c)

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__param['function'](self.__problem_parameters["furniture"], c.representation,
                                                 self.__problem_parameters["budget"])

    def best_chromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.fitness < best.fitness:
                best = c
        return best

    def selection(self):
        pos1 = randint(0, self.__param['popSize'] - 1)
        pos2 = randint(0, self.__param['popSize'] - 1)
        if self.__population[pos1].fitness < self.__population[pos2].fitness:
            return pos1
        else:
            return pos2
