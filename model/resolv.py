from model.chromosome import MyChromosome
from model.genetic_algorithm import GA
from model.utils import get_index_off_generated
from model.utils_ga import evaluation, get_right_furniture


class Resolver:
    def __init__(self, budget, furniture, already_generated=[]):
        self.__ga = None
        self.__budget = budget
        self.__furniture = get_right_furniture(furniture)
        self.__already_generated = already_generated
        self.__indexes_generated = []

    @property
    def furniture(self):
        return self.__furniture

    def set_index_generated(self):
        if self.__already_generated is not None:
            self.__indexes_generated = get_index_off_generated(self.__already_generated, self.__furniture)

    def get_furniture_from_bests(self, bests):
        list_available = []
        final_res = bests[0]
        pos = 0
        for type_f in self.__furniture.keys():
            list_available.append(self.__furniture[type_f][final_res.representation[pos]])
            pos = pos + 1

        return list_available

    def make_ga(self, population_size=300, no_of_generations=100, evaluation_function=evaluation,
                chromosome=MyChromosome):
        genetic_parameters = {
            "popSize": population_size,
            "noGen": no_of_generations,
            "function": evaluation_function,
            "chromosome": chromosome
        }
        problem_parameters = {
            "furniture": self.__furniture,
            "budget": self.__budget,
            "generated": self.__already_generated
        }
        self.__ga = GA(genetic_parameters, problem_parameters)

    def find_furniture(self):
        self.__ga.initialisation()
        self.__ga.evaluation()
        bests = []
        last_gens = []

        for generation in range(self.__ga.param["noGen"]):
            # ga.oneGeneration()
            self.__ga.oneGenerationElitism()
            # ga.oneGenerationSteadyState()
            best_chromosome = self.__ga.bestChromosome()
            last_gens = self.__ga.population
            if best_chromosome not in bests:
                bests.append(best_chromosome)

        the_best = bests[0]
        for best in bests:
            if best.fitness < the_best.fitness:
                the_best = best

        the_bests = [the_best]

        for candidate in last_gens:
            if candidate.fitness < the_bests[0].fitness:
                the_bests = [candidate]
            elif candidate.fitness == the_best.fitness and candidate not in the_bests:
                the_bests.append(candidate)

        return self.get_furniture_from_bests(the_bests)
