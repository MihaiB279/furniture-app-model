from model.chromosome import MyChromosome
from model.clustering import cluster_item
from model.genetic_algorithm import GA
from model.utils import get_index_off_generated, get_list, check_all_no_preference
from model.utils_ga import evaluation
from requests.classes_for_requestst import Furniture


class Resolver:
    def __init__(self, budget, furniture, already_generated=[]):
        self.__ga = None
        self.__budget = budget
        self.__furniture = self.get_right_furniture(furniture)
        self.__already_generated = already_generated
        self.__indexes_generated = []

    @property
    def furniture(self):
        return self.__furniture

    def get_right_furniture(self, furniture_details):
        furniture = []
        for single_furniture in furniture_details:
            checked_furniture = False
            name = single_furniture.furnitureType
            details_as_dict = get_list(single_furniture.details)
            furniture_available = cluster_item(name, details_as_dict)
            for item in furniture_available:
                is_good = True
                for attribute_name, attribute_value in details_as_dict.items():
                    if attribute_value != "No preferences" and (
                            attribute_name not in item[0].keys() or attribute_value != item[0][attribute_name]):
                        is_good = False
                        break
                if is_good:
                    furniture.append(item)
                    checked_furniture = True
                    break
            if checked_furniture is False:
                if check_all_no_preference(details_as_dict):
                    furniture.append(furniture_available[0])
                else:
                    return name
        return furniture

    def set_index_generated(self):
        if self.__already_generated is not None:
            self.__indexes_generated = get_index_off_generated(self.__already_generated, self.__furniture)

    def get_furniture_from_bests(self, bests):
        list_available = []
        final_res = bests[0]
        pos = 0
        for furniture_list in self.__furniture:
            list_available.append(furniture_list[final_res.representation[pos]])
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
            "generated": self.__indexes_generated
        }
        self.__ga = GA(genetic_parameters, problem_parameters)

    def find_furniture(self):
        self.__ga.initialisation()
        self.__ga.evaluation()
        bests = []
        last_gens = []

        for generation in range(self.__ga.param["noGen"]):
            self.__ga.oneGenerationElitism()
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

    def construct_furniture(self, furniture_string):
        furniture = Furniture(
            furnitureType="",
            name="",
            company="",
            details="",
            price=0.0
        )
        index = furniture_string.find(", 'Price':")

        details = furniture_string[:index]
        rest_furniture = furniture_string[index + 1:].strip()
        parts = get_list(rest_furniture)

        for key, value in parts.items():
            good_key = key.strip().strip("'")
            good_value = value.strip().strip("'")
            if good_key == "Price":
                furniture.price = float(good_value)
            elif good_key == "Company":
                furniture.company = good_value
            elif good_key == "Name":
                furniture.name = good_value
            elif good_key == "Furniture Type":
                furniture.furnitureType = good_value.strip('\'}')

        furniture.details = details.strip()
        return furniture
